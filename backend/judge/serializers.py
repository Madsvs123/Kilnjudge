from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from rest_framework import serializers

from .catalog import TAG_LABELS
from .models import Editorial, Hint, Problem, ProblemTest, Submission, Tag

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(r"^[A-Za-z0-9_]{3,150}$")
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = ("id", "username", "password")
        read_only_fields = ("id",)

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )


class SampleTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTest
        fields = ("input_data", "expected_output")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "label")


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ("position", "body")


class ProblemListSerializer(serializers.ModelSerializer):
    sample_count = serializers.IntegerField(read_only=True)
    hidden_count = serializers.IntegerField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = (
            "slug",
            "title",
            "position",
            "difficulty",
            "tags",
            "summary",
            "time_limit_ms",
            "sample_count",
            "hidden_count",
        )


class ProblemDetailSerializer(serializers.ModelSerializer):
    samples = serializers.SerializerMethodField()
    hidden_count = serializers.IntegerField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    hints = HintSerializer(many=True, read_only=True)
    editorial = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = (
            "slug",
            "title",
            "position",
            "difficulty",
            "tags",
            "summary",
            "statement",
            "input_format",
            "output_format",
            "time_limit_ms",
            "hidden_count",
            "hints",
            "editorial",
            "samples",
        )

    def get_editorial(self, problem: Problem):
        try:
            editorial = problem.editorial
        except ObjectDoesNotExist:
            return None
        return {"notes": editorial.notes, "updated_at": editorial.updated_at}

    def get_samples(self, problem: Problem):
        samples = problem.tests.filter(is_sample=True)
        return SampleTestSerializer(samples, many=True).data


class ProblemTestWriteSerializer(serializers.Serializer):
    input_data = serializers.CharField(max_length=20_000, allow_blank=True, trim_whitespace=False)
    expected_output = serializers.CharField(max_length=20_000, allow_blank=True, trim_whitespace=False)
    is_sample = serializers.BooleanField()


class ProblemCreateSerializer(serializers.Serializer):
    slug = serializers.RegexField(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=80)
    title = serializers.CharField(max_length=120)
    difficulty = serializers.ChoiceField(choices=["intro", "medium", "hard"])
    summary = serializers.CharField(max_length=240)
    statement = serializers.CharField(max_length=8000)
    input_format = serializers.CharField(max_length=2000)
    output_format = serializers.CharField(max_length=2000)
    time_limit_ms = serializers.IntegerField(min_value=200, max_value=10_000, default=2000)
    tags = serializers.ListField(
        child=serializers.SlugField(max_length=40),
        required=False,
        default=list,
        max_length=8,
    )
    tests = ProblemTestWriteSerializer(many=True, min_length=2, max_length=40)

    def validate_slug(self, value: str) -> str:
        if Problem.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A problem with this slug already exists.")
        return value

    def validate_tests(self, tests):
        if not any(test["is_sample"] for test in tests):
            raise serializers.ValidationError("Include at least one sample test.")
        if not any(not test["is_sample"] for test in tests):
            raise serializers.ValidationError("Include at least one hidden test.")
        return tests

    def create(self, validated_data):
        tests = validated_data.pop("tests")
        tag_slugs = validated_data.pop("tags", [])
        next_position = (Problem.objects.aggregate(Max("position"))["position__max"] or 0) + 1
        problem = Problem.objects.create(position=next_position, **validated_data)
        for position, test in enumerate(tests, start=1):
            ProblemTest.objects.create(
                problem=problem,
                position=position,
                input_data=test["input_data"],
                expected_output=test["expected_output"],
                is_sample=test["is_sample"],
            )
        chosen = []
        for slug in tag_slugs:
            tag, _created = Tag.objects.get_or_create(
                slug=slug,
                defaults={"label": TAG_LABELS.get(slug, slug.replace("-", " ").title())},
            )
            chosen.append(tag)
        if chosen:
            problem.tags.set(chosen)
        return problem


class EditorialWriteSerializer(serializers.Serializer):
    notes = serializers.CharField(allow_blank=True, max_length=8000, trim_whitespace=False)


class SubmitSerializer(serializers.Serializer):
    source_code = serializers.CharField(
        max_length=100_000,
        allow_blank=False,
        trim_whitespace=False,
    )

    def validate_source_code(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Write a Python solution before submitting.")
        return value


class SubmissionSerializer(serializers.ModelSerializer):
    problem_slug = serializers.CharField(source="problem.slug", read_only=True)
    problem_title = serializers.CharField(source="problem.title", read_only=True)

    class Meta:
        model = Submission
        fields = (
            "id",
            "problem_slug",
            "problem_title",
            "verdict",
            "runtime_ms",
            "message",
            "source_code",
            "created_at",
        )
