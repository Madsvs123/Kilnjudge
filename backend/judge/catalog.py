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
        "hints": [
            "Skip the first reading and the last reading. A valley needs a neighbor on both sides.",
            "If either neighbor is less than or equal to the reading, that reading is not a valley.",
        ],
        "editorial": (
            "Walk from the second reading through the second-to-last. Count a reading only when "
            "it is strictly colder than both neighbors. The end readings have only one neighbor, "
            "so they stay out of the count."
        ),
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
        "hints": [
            "Stop when the current value has one digit. Reaching that digit is not an extra step.",
            "Each replacement looks only at the decimal digits of the current value.",
        ],
        "editorial": (
            "Keep replacing the number while it is at least 10. Each replacement is the sum of "
            "the squares of its decimal digits, and each replacement counts as one step. A value "
            "that is already below 10 contributes zero steps."
        ),
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
        "hints": [
            "A positive even distance means the two indexes are different and have the same parity.",
            "Count each letter on even indexes separately from the same letter on odd indexes.",
        ],
        "editorial": (
            "Indexes an even distance apart share a parity. For each letter, count occurrences "
            "on even indexes and occurrences on odd indexes. A group of k matching indexes "
            "contributes one twin for every way to choose two of them."
        ),
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
        "hints": [
            "Collapse adjacent equal values into one block before you look for an increase.",
            "The answer counts original elements. A long flat block can outweigh several short rises.",
        ],
        "editorial": (
            "First compress the array into blocks of equal values, keeping each block's length. "
            "Then scan the blocks from left to right. Extend the current cover while the block "
            "values strictly increase, and restart the cover when they do not. Remember the "
            "largest cover, measured in original elements."
        ),
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
    {
        "slug": "shelf-gaps",
        "title": "Shelf Gaps",
        "position": 5,
        "difficulty": "intro",
        "tags": ["arrays", "counting"],
        "summary": "Count tiles that stand strictly taller than the tile two places to the right.",
        "time_limit_ms": 1000,
        "statement": (
            "A drying shelf holds tiles in a single row. Each tile has an integer height. "
            "A shelf gap opens at a tile when that tile is strictly taller than the tile "
            "two places to its right. The tile immediately to the right is ignored.\n\n"
            "The last two tiles never open a gap, because nothing sits two places beyond them. "
            "Equal heights do not open a gap.\n\n"
            "On the shelf 5 3 4 1 2, the tile 5 is taller than 4, the tile 3 is taller than 1, "
            "and the tile 4 is taller than 2, so the answer is 3. On the shelf 1 2 3 4 every "
            "later tile is taller, so the answer is 0. On the shelf 4 1 4 1 the compared pairs "
            "are equal, so the answer is 0."
        ),
        "input_format": (
            "The first line holds an integer n, the number of tiles.\n"
            "The second line holds n integers, the heights from left to right.\n"
            "1 <= n <= 1000. Each height is a 32-bit signed integer."
        ),
        "output_format": "Print a single integer, the number of shelf gaps.",
        "hints": [
            "Compare a tile with the tile two places to its right, not with its immediate neighbor.",
            "The last two tiles have nothing two places further along, so they do not open a gap.",
        ],
        "editorial": (
            "Look at indexes 0 through n - 3. A gap exists at i when the height at i is strictly "
            "greater than the height at i + 2. The immediate neighbor is not part of the comparison."
        ),
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "5\n5 3 4 1 2\n", "expected_output": "3\n"},
            {"position": 2, "is_sample": True, "input_data": "4\n1 2 3 4\n", "expected_output": "0\n"},
            {"position": 3, "is_sample": True, "input_data": "4\n4 1 4 1\n", "expected_output": "0\n"},
            {"position": 4, "is_sample": False, "input_data": "1\n42\n", "expected_output": "0\n"},
            {"position": 5, "is_sample": False, "input_data": "5\n8 1 7 2 6\n", "expected_output": "2\n"},
            {"position": 6, "is_sample": False, "input_data": "4\n3 3 3 3\n", "expected_output": "0\n"},
            {"position": 7, "is_sample": False, "input_data": "6\n2 9 1 8 0 7\n", "expected_output": "4\n"},
        ],
    },
    {
        "slug": "glaze-runs",
        "title": "Glaze Runs",
        "position": 6,
        "difficulty": "intro",
        "tags": ["strings"],
        "summary": "Sum the squared lengths of maximal blocks of the same letter.",
        "time_limit_ms": 1000,
        "statement": (
            "A glaze code is one line of lowercase English letters. A run is a maximal "
            "contiguous block of the same letter. The weight of a run is the square of "
            "its length. Add the weights of every run.\n\n"
            "The code aabccc has runs of length 2, 1, and 3. Their weights are 4, 1, and 9, "
            "so the answer is 14. The code abcd is four runs of length 1, so the answer is 4. "
            "The code aaa is one run of length 3, so the answer is 9."
        ),
        "input_format": (
            "One line holding the glaze code s.\n"
            "1 <= length of s <= 1000. Every character is a lowercase English letter."
        ),
        "output_format": "Print a single integer, the sum of the squared run lengths.",
        "hints": [
            "Close a run when the letter changes, and close the final run at the end of the string.",
            "Square each run length on its own, then add those squares.",
        ],
        "editorial": (
            "Scan the string once and keep the length of the current run. When the letter changes, "
            "add the square of that length to the total and start a new run. After the scan, add "
            "the square of the final run as well."
        ),
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "aabccc\n", "expected_output": "14\n"},
            {"position": 2, "is_sample": True, "input_data": "abcd\n", "expected_output": "4\n"},
            {"position": 3, "is_sample": True, "input_data": "aaa\n", "expected_output": "9\n"},
            {"position": 4, "is_sample": False, "input_data": "a\n", "expected_output": "1\n"},
            {"position": 5, "is_sample": False, "input_data": "book\n", "expected_output": "6\n"},
            {"position": 6, "is_sample": False, "input_data": "mississippi\n", "expected_output": "17\n"},
            {"position": 7, "is_sample": False, "input_data": "aaabaaa\n", "expected_output": "19\n"},
        ],
    },
    {
        "slug": "pair-kiln-totals",
        "title": "Pair Kiln Totals",
        "position": 7,
        "difficulty": "medium",
        "tags": ["math", "arrays"],
        "summary": "Count unordered pairs of temperatures whose sum is divisible by three.",
        "time_limit_ms": 1500,
        "statement": (
            "A firing log lists integer temperatures. Count the unordered pairs of distinct "
            "positions whose temperatures add up to a multiple of 3. A temperature is never "
            "paired with itself, and the pair (left, right) is the same pair as (right, left).\n\n"
            "On the log 1 2 3 4 the pairs are 1+2 and 2+4. Both sums are multiples of 3, and "
            "the other four pairs are not, so the answer is 2. A single temperature has no "
            "pair, so the answer is 0. Three equal temperatures that are 1 mod 3, such as "
            "1 1 1, never sum to a multiple of 3, so the answer is 0."
        ),
        "input_format": (
            "The first line holds an integer n, the number of temperatures.\n"
            "The second line holds n integers.\n"
            "1 <= n <= 1000. Each temperature is an integer from 0 through 10000."
        ),
        "output_format": "Print a single integer, the number of pairs.",
        "hints": [
            "A pair uses two different positions. Swapping those positions does not make a new pair.",
            "You only need to know whether a sum is a multiple of 3.",
        ],
        "editorial": (
            "Group the temperatures by remainder modulo 3. Two remainder-0 values form a valid "
            "pair, and every remainder-1 value forms a valid pair with every remainder-2 value. "
            "Two values that share remainder 1, or that share remainder 2, do not."
        ),
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "4\n1 2 3 4\n", "expected_output": "2\n"},
            {"position": 2, "is_sample": True, "input_data": "1\n3\n", "expected_output": "0\n"},
            {"position": 3, "is_sample": True, "input_data": "3\n1 1 1\n", "expected_output": "0\n"},
            {"position": 4, "is_sample": False, "input_data": "3\n3 6 9\n", "expected_output": "3\n"},
            {"position": 5, "is_sample": False, "input_data": "5\n1 2 2 4 5\n", "expected_output": "6\n"},
            {"position": 6, "is_sample": False, "input_data": "3\n0 0 0\n", "expected_output": "3\n"},
            {"position": 7, "is_sample": False, "input_data": "2\n4 5\n", "expected_output": "1\n"},
        ],
    },
    {
        "slug": "balanced-stamp-windows",
        "title": "Balanced Stamp Windows",
        "position": 8,
        "difficulty": "hard",
        "tags": ["strings", "ranges"],
        "summary": "Count contiguous windows that contain the same number of a and b.",
        "time_limit_ms": 2500,
        "statement": (
            "A kiln stamp is a string made only of the letters a and b. A window is any "
            "contiguous block of the stamp, including a block of one letter and the whole "
            "stamp. A window is balanced when it contains the same number of a letters as "
            "b letters. Count the balanced windows.\n\n"
            "The stamp ab has one balanced window, the whole stamp. The stamp aabb has the "
            "window ab in the middle and the whole stamp, so the answer is 2. The stamp abba "
            "has ab, ba, and the whole stamp, so the answer is 3. A window of odd length "
            "cannot be balanced."
        ),
        "input_format": (
            "One line holding the stamp s.\n"
            "1 <= length of s <= 200. Every character is a or b."
        ),
        "output_format": "Print a single integer, the number of balanced windows.",
        "hints": [
            "A window of odd length cannot hold the same count of each letter.",
            "Count every contiguous block, including blocks that sit strictly inside the stamp.",
        ],
        "editorial": (
            "Odd-length windows cannot balance. For each start index, grow the window to the right "
            "and keep a count of a and a count of b. Whenever those counts match, the window is "
            "one answer. The length bound of 200 keeps this double scan inside the time limit."
        ),
        "tests": [
            {"position": 1, "is_sample": True, "input_data": "ab\n", "expected_output": "1\n"},
            {"position": 2, "is_sample": True, "input_data": "aabb\n", "expected_output": "2\n"},
            {"position": 3, "is_sample": True, "input_data": "abba\n", "expected_output": "3\n"},
            {"position": 4, "is_sample": False, "input_data": "a\n", "expected_output": "0\n"},
            {"position": 5, "is_sample": False, "input_data": "aa\n", "expected_output": "0\n"},
            {"position": 6, "is_sample": False, "input_data": "abab\n", "expected_output": "4\n"},
            {"position": 7, "is_sample": False, "input_data": "bbb\n", "expected_output": "0\n"},
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
