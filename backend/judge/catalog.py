"""Original practice problems shipped with Kilnjudge.

These exercises were written for this project. They are not taken from a contest archive.
"""

PROBLEMS = [
    {
        "slug": "interior-valleys",
        "title": "Interior Valleys",
        "position": 1,
        "difficulty": "intro",
        "tags": ["arrays", "counting"],
        "summary": "Count readings that are strictly colder than both neighbors.",
        "time_limit_ms": 2000,
        "statement": (
            "A firing curve is a sequence of integer temperature readings. "
            "An interior valley is any reading, other than the first or the last, "
            "that is strictly colder than both of its immediate neighbors.\n\n"
            "Equal neighbors do not make a valley. Count the valleys.\n\n"
            "On the curve 3 1 4 2 5, the reading 1 is colder than 3 and 4, and the "
            "reading 2 is colder than 4 and 5, so the answer is 2. On the curve "
            "5 1 1 5, the two middle readings are equal, so neither is a strict "
            "valley and the answer is 0."
        ),
        "input_format": (
            "The first line holds an integer n, the number of readings.\n"
            "The second line holds n integers, the readings from left to right.\n"
            "1 <= n <= 1000. Each reading is a 32-bit signed integer."
        ),
        "output_format": "Print a single integer, the number of interior valleys.",
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "5\n3 1 4 2 5\n", "expected_output": "2\n"},
            {"position": 2, "is_sample": True, "input_data": "3\n1 2 3\n", "expected_output": "0\n"},
            {"position": 3, "is_sample": True, "input_data": "4\n5 1 1 5\n", "expected_output": "0\n"},
            {"position": 4, "is_sample": False, "input_data": "1\n42\n", "expected_output": "0\n"},
            {"position": 5, "is_sample": False, "input_data": "6\n1 0 1 0 1 0\n", "expected_output": "2\n"},
            {"position": 6, "is_sample": False, "input_data": "7\n9 1 8 2 7 0 6\n", "expected_output": "3\n"},
            {"position": 7, "is_sample": False, "input_data": "4\n2 2 2 2\n", "expected_output": "0\n"},
        ],
    },
    {
        "slug": "square-digit-steps",
        "title": "Square Digit Steps",
        "position": 2,
        "difficulty": "intro",
        "tags": ["math", "digits"],
        "summary": "Count replacements by the sum of squared decimal digits until one digit remains.",
        "time_limit_ms": 2000,
        "statement": (
            "Start with a non-negative integer. While the number still has two or more digits, "
            "replace it with the sum of the squares of its decimal digits. Count how many "
            "replacements you make. Stop when a single digit remains. A number that is already "
            "a single digit takes no steps.\n\n"
            "25 becomes 2^2 + 5^2 = 29, then 85, 89, 145, 42, 20, and finally 4. "
            "That is 7 replacements. 10 becomes 1^2 + 0^2 = 1, which is 1 replacement."
        ),
        "input_format": (
            "One line holding an integer n.\n"
            "0 <= n <= 1000000000."
        ),
        "output_format": "Print a single integer, the number of replacements.",
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "5\n", "expected_output": "0\n"},
            {"position": 2, "is_sample": True, "input_data": "25\n", "expected_output": "7\n"},
            {"position": 3, "is_sample": True, "input_data": "10\n", "expected_output": "1\n"},
            {"position": 4, "is_sample": False, "input_data": "0\n", "expected_output": "0\n"},
            {"position": 5, "is_sample": False, "input_data": "2026\n", "expected_output": "5\n"},
            {"position": 6, "is_sample": False, "input_data": "99\n", "expected_output": "12\n"},
            {"position": 7, "is_sample": False, "input_data": "81\n", "expected_output": "9\n"},
        ],
    },
    {
        "slug": "even-gap-twins",
        "title": "Even-Gap Twins",
        "position": 3,
        "difficulty": "medium",
        "tags": ["strings", "counting"],
        "summary": "Count matching letters whose indexes are a positive even distance apart.",
        "time_limit_ms": 2000,
        "statement": (
            "A kiln stamp is one line of lowercase English letters. Two indexes form an "
            "even-gap twin when they carry the same letter, the left index is strictly smaller, "
            "and the distance between them is positive and even.\n\n"
            "Indexes are 0-based. The distance is even exactly when the two indexes have the "
            "same parity. Count the twins.\n\n"
            "In aba the two a characters sit at indexes 0 and 2. Their distance is 2, so the "
            "answer is 1. In aaaa the indexes are 0, 1, 2, and 3. The pairs (0, 2) and (1, 3) "
            "are twins. Pairs with an odd distance are not. The answer is 2. In abba every "
            "matching pair has an odd distance, so the answer is 0."
        ),
        "input_format": (
            "One line holding the stamp s.\n"
            "1 <= length of s <= 1000. Every character is a lowercase English letter."
        ),
        "output_format": "Print a single integer, the number of even-gap twins.",
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "aba\n", "expected_output": "1\n"},
            {"position": 2, "is_sample": True, "input_data": "aaaa\n", "expected_output": "2\n"},
            {"position": 3, "is_sample": True, "input_data": "abba\n", "expected_output": "0\n"},
            {"position": 4, "is_sample": False, "input_data": "a\n", "expected_output": "0\n"},
            {"position": 5, "is_sample": False, "input_data": "ababab\n", "expected_output": "6\n"},
            {"position": 6, "is_sample": False, "input_data": "bookkeeper\n", "expected_output": "1\n"},
            {"position": 7, "is_sample": False, "input_data": "mississippi\n", "expected_output": "4\n"},
        ],
    },
    {
        "slug": "rising-plateau-cover",
        "title": "Rising Plateau Cover",
        "position": 4,
        "difficulty": "medium",
        "tags": ["arrays", "ranges"],
        "summary": "Find the longest stretch of strictly rising equal-value blocks.",
        "time_limit_ms": 2000,
        "statement": (
            "Group the array into plateaus. A plateau is a maximal contiguous block of equal values.\n\n"
            "Read the plateaus from left to right. A rising run is a contiguous sequence of these "
            "plateaus whose values strictly increase. Its cover is the number of original array "
            "elements inside it. A single plateau is a rising run on its own.\n\n"
            "The array 1 1 2 2 2 1 3 3 breaks into plateaus of value 1 (length 2), 2 (length 3), "
            "1 (length 1), and 3 (length 2). The first two plateaus rise and cover 5 elements. "
            "The last two rise and cover 3. The largest cover is 5.\n\n"
            "The array 5 4 3 2 never rises, so each plateau stands alone and the largest cover is 1. "
            "The array 2 2 2 is one plateau, so its cover is 3."
        ),
        "input_format": (
            "The first line holds an integer n, the length of the array.\n"
            "The second line holds n integers.\n"
            "1 <= n <= 1000. Each value is a 32-bit signed integer."
        ),
        "output_format": "Print a single integer, the largest rising-run cover.",
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "8\n1 1 2 2 2 1 3 3\n", "expected_output": "5\n"},
            {"position": 2, "is_sample": True, "input_data": "4\n5 4 3 2\n", "expected_output": "1\n"},
            {"position": 3, "is_sample": True, "input_data": "4\n1 2 3 4\n", "expected_output": "4\n"},
            {"position": 4, "is_sample": False, "input_data": "3\n2 2 2\n", "expected_output": "3\n"},
            {"position": 5, "is_sample": False, "input_data": "7\n1 3 3 2 4 4 5\n", "expected_output": "4\n"},
            {"position": 6, "is_sample": False, "input_data": "7\n8 8 1 1 2 2 9\n", "expected_output": "5\n"},
            {"position": 7, "is_sample": False, "input_data": "1\n1\n", "expected_output": "1\n"},
        ],
    },
]


TAG_LABELS = {
    "arrays": "Arrays",
    "counting": "Counting",
    "digits": "Digits",
    "math": "Math",
    "ranges": "Ranges",
    "strings": "Strings",
}


def load_catalog(problem_model, test_model, tag_model=None, hint_model=None, editorial_model=None) -> None:
    field_names = (
        "title",
        "position",
        "difficulty",
        "summary",
        "statement",
        "input_format",
        "output_format",
        "time_limit_ms",
    )
    concrete = {field.name for field in problem_model._meta.fields}
    for entry in PROBLEMS:
        defaults = {name: entry[name] for name in field_names if name in concrete}
        problem, _created = problem_model.objects.update_or_create(
            slug=entry["slug"],
            defaults=defaults,
        )
        _assign_tags(problem, entry, tag_model)
        _assign_hints(problem, entry, hint_model)
        _assign_editorial(problem, entry, editorial_model)
        positions = [test["position"] for test in entry["tests"]]
        test_model.objects.filter(problem=problem).exclude(position__in=positions).delete()
        for test in entry["tests"]:
            test_model.objects.update_or_create(
                problem=problem,
                position=test["position"],
                defaults={
                    "input_data": test["input_data"],
                    "expected_output": test["expected_output"],
                    "is_sample": test["is_sample"],
                },
            )


def _assign_tags(problem, entry, tag_model) -> None:
    if tag_model is None or not hasattr(problem, "tags"):
        return
    chosen = []
    for slug in entry.get("tags", []):
        tag, _created = tag_model.objects.update_or_create(
            slug=slug,
            defaults={"label": TAG_LABELS.get(slug, slug.replace("-", " ").title())},
        )
        chosen.append(tag)
    problem.tags.set(chosen)


def _assign_hints(problem, entry, hint_model) -> None:
    if hint_model is None:
        return
    bodies = list(entry.get("hints", []))
    hint_model.objects.filter(problem=problem).exclude(position__in=range(1, len(bodies) + 1)).delete()
    for position, body in enumerate(bodies, start=1):
        hint_model.objects.update_or_create(
            problem=problem,
            position=position,
            defaults={"body": body},
        )


def _assign_editorial(problem, entry, editorial_model) -> None:
    if editorial_model is None or "editorial" not in entry:
        return
    editorial_model.objects.update_or_create(
        problem=problem,
        defaults={"notes": entry["editorial"]},
    )
