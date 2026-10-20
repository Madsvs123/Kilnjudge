from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from judge.models import Problem, ProblemTest, Submission

User = get_user_model()

CORRECT_ADD = "a, b = map(int, input().split())\nprint(a + b)\n"
WRONG_ADD = "print(0)\n"
SAMPLE_ONLY = "a, b = map(int, input().split())\nprint(a + b if a > 0 else 9)\n"


class SolutionVerdictTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("kiln-owner", password="local-pass-123")
        self.problem = Problem.objects.create(
            slug="add-two",
            title="Add Two",
            position=100,
            difficulty="intro",
            summary="Add a pair of integers.",
            statement="Read two integers and print their sum.",
            input_format="One line with two integers a and b.",
            output_format="One integer, a + b.",
            time_limit_ms=2000,
        )
        ProblemTest.objects.create(
            problem=self.problem,
            position=1,
            input_data="2 3\n",
            expected_output="5\n",
            is_sample=True,
        )
        ProblemTest.objects.create(
            problem=self.problem,
            position=2,
            input_data="-4 4\n",
            expected_output="0\n",
            is_sample=False,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.owner)
        self.submit_url = reverse("submit", kwargs={"slug": "add-two"})

    def test_correct_solution_is_accepted(self):
        response = self.client.post(self.submit_url, {"source_code": CORRECT_ADD}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["verdict"], Submission.VERDICT_ACCEPTED)
        stored = Submission.objects.get(pk=response.data["id"])
        self.assertEqual(stored.owner, self.owner)
        self.assertEqual(stored.verdict, Submission.VERDICT_ACCEPTED)
        self.assertIn("Passed", stored.message)

    def test_wrong_solution_is_rejected(self):
        response = self.client.post(self.submit_url, {"source_code": WRONG_ADD}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["verdict"], Submission.VERDICT_WRONG)
        self.assertNotEqual(response.data["verdict"], Submission.VERDICT_ACCEPTED)
        stored = Submission.objects.get(pk=response.data["id"])
        self.assertEqual(stored.verdict, Submission.VERDICT_WRONG)

    def test_sample_check_does_not_store_a_submission(self):
        response = self.client.post(
            reverse("sample-run", kwargs={"slug": "add-two"}),
            {"source_code": SAMPLE_ONLY},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["verdict"], Submission.VERDICT_ACCEPTED)
        self.assertFalse(response.data["stored"])
        self.assertIn("Hidden tests were not run", response.data["message"])
        self.assertEqual(Submission.objects.count(), 0)

    def test_hidden_test_rejects_a_sample_only_solution(self):
        response = self.client.post(self.submit_url, {"source_code": SAMPLE_ONLY}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["verdict"], Submission.VERDICT_WRONG)
        self.assertIn("hidden", response.data["message"])
        self.assertNotIn("-4", response.data["message"])
        self.assertNotIn("expected", response.data["message"].lower())

    def test_problem_payload_keeps_hidden_tests_on_the_server(self):
        response = self.client.get(reverse("problem-detail", kwargs={"slug": "add-two"}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["samples"]), 1)
        self.assertEqual(response.data["samples"][0]["input_data"], "2 3\n")
        self.assertEqual(response.data["hidden_count"], 1)
        self.assertNotContains(response, "-4 4")

    def test_submission_history_belongs_to_the_signed_in_owner(self):
        self.client.post(self.submit_url, {"source_code": CORRECT_ADD}, format="json")
        other = User.objects.create_user("other-owner", password="local-pass-123")
        other_client = APIClient()
        other_client.force_authenticate(other)

        own_history = self.client.get(reverse("submission-list"))
        other_history = other_client.get(reverse("submission-list"))
        own_id = own_history.data[0]["id"]
        stolen = other_client.get(reverse("submission-detail", kwargs={"pk": own_id}))

        self.assertEqual(len(own_history.data), 1)
        self.assertEqual(other_history.status_code, 200)
        self.assertEqual(other_history.data, [])
        self.assertEqual(stolen.status_code, 404)

    def test_problem_time_limit_stops_a_slow_solution(self):
        self.problem.time_limit_ms = 400
        self.problem.save(update_fields=["time_limit_ms"])
        source = "while True:\n    pass\n"

        response = self.client.post(self.submit_url, {"source_code": source}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["verdict"], Submission.VERDICT_TIME_LIMIT)
        self.assertIn("400", response.data["message"])

    def test_network_socket_is_rejected(self):
        source = "import socket\nsocket.socket()\n"
        response = self.client.post(self.submit_url, {"source_code": source}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["verdict"], Submission.VERDICT_RUNTIME)

    def test_catalog_seeds_four_original_problems(self):
        expected = {
            "interior-valleys",
            "square-digit-steps",
            "even-gap-twins",
            "rising-plateau-cover",
        }
        seeded = Problem.objects.filter(slug__in=expected)
        self.assertEqual(seeded.count(), 4)
        for problem in seeded:
            self.assertGreaterEqual(problem.tests.filter(is_sample=True).count(), 3)
            self.assertGreaterEqual(problem.tests.filter(is_sample=False).count(), 3)
