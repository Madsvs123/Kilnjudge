from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Problem, ProblemTest, Submission

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


class ProblemListSerializer(serializers.ModelSerializer):
    sample_count = serializers.IntegerField(read_only=True)
    hidden_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Problem
        fields = (
            "slug",
            "title",
            "position",
            "difficulty",
            "summary",
            "time_limit_ms",
            "sample_count",
            "hidden_count",
        )


class ProblemDetailSerializer(serializers.ModelSerializer):
    samples = serializers.SerializerMethodField()
    hidden_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Problem
        fields = (
            "slug",
            "title",
            "position",
            "difficulty",
            "summary",
            "statement",
            "input_format",
            "output_format",
            "time_limit_ms",
            "hidden_count",
            "samples",
        )

    def get_samples(self, problem: Problem):
        samples = problem.tests.filter(is_sample=True)
        return SampleTestSerializer(samples, many=True).data


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
