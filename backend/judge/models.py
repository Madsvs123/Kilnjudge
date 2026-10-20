from django.conf import settings
from django.db import models


class Problem(models.Model):
    DIFFICULTY_CHOICES = (
        ("intro", "Intro"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    )

    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=120)
    position = models.PositiveIntegerField(unique=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    summary = models.CharField(max_length=240)
    statement = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    time_limit_ms = models.PositiveIntegerField(default=2000)
    tags = models.ManyToManyField("Tag", related_name="problems", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "title"]

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    slug = models.SlugField(max_length=40, unique=True)
    label = models.CharField(max_length=40)

    class Meta:
        ordering = ["label", "slug"]

    def __str__(self) -> str:
        return self.label


class ProblemTest(models.Model):
    problem = models.ForeignKey(Problem, related_name="tests", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["problem", "position"],
                name="unique_problem_test_position",
            )
        ]

    def __str__(self) -> str:
        kind = "sample" if self.is_sample else "hidden"
        return f"{self.problem.slug} {kind} {self.position}"


class Hint(models.Model):
    problem = models.ForeignKey(Problem, related_name="hints", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    body = models.TextField()

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["problem", "position"],
                name="unique_problem_hint_position",
            )
        ]

    def __str__(self) -> str:
        return f"{self.problem.slug} hint {self.position}"


class Editorial(models.Model):
    problem = models.OneToOneField(Problem, related_name="editorial", on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.problem.slug} editorial"


class Submission(models.Model):
    VERDICT_ACCEPTED = "accepted"
    VERDICT_WRONG = "wrong_answer"
    VERDICT_TIME_LIMIT = "time_limit"
    VERDICT_RUNTIME = "runtime_error"
    VERDICT_CHOICES = (
        (VERDICT_ACCEPTED, "Accepted"),
        (VERDICT_WRONG, "Wrong Answer"),
        (VERDICT_TIME_LIMIT, "Time Limit"),
        (VERDICT_RUNTIME, "Runtime Error"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="submissions",
        on_delete=models.CASCADE,
    )
    problem = models.ForeignKey(Problem, related_name="submissions", on_delete=models.CASCADE)
    source_code = models.TextField()
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES)
    runtime_ms = models.PositiveIntegerField(default=0)
    message = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["owner", "-created_at"])]

    def __str__(self) -> str:
        return f"{self.owner} {self.problem.slug} {self.verdict}"
