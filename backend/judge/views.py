import difflib

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Editorial, Problem, Submission, Tag
from .runner import run_source
from .serializers import (
    EditorialWriteSerializer,
    ProblemCreateSerializer,
    ProblemDetailSerializer,
    ProblemListSerializer,
    RegisterSerializer,
    TagSerializer,
    SubmissionSerializer,
    SubmitSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    def get(self, request):
        return Response({"username": request.user.username})


def _annotated_problems():
    return Problem.objects.prefetch_related("tags", "hints", "editorial").annotate(
        sample_count=Count("tests", filter=Q(tests__is_sample=True)),
        hidden_count=Count("tests", filter=Q(tests__is_sample=False)),
    )


class ProblemListView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProblemCreateSerializer
        return ProblemListSerializer

    def get_queryset(self):
        queryset = _annotated_problems()
        tag = (self.request.query_params.get("tag") or "").strip()
        if tag:
            queryset = queryset.filter(tags__slug=tag).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        incoming = self.get_serializer(data=request.data)
        incoming.is_valid(raise_exception=True)
        problem = incoming.save()
        annotated = _annotated_problems().get(pk=problem.pk)
        return Response(ProblemDetailSerializer(annotated).data, status=status.HTTP_201_CREATED)


class TagListView(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ProblemDetailView(generics.RetrieveAPIView):
    serializer_class = ProblemDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return _annotated_problems()


class EditorialView(APIView):
    def put(self, request, slug):
        problem = get_object_or_404(Problem, slug=slug)
        incoming = EditorialWriteSerializer(data=request.data)
        incoming.is_valid(raise_exception=True)
        editorial, _created = Editorial.objects.update_or_create(
            problem=problem,
            defaults={"notes": incoming.validated_data["notes"]},
        )
        return Response({"notes": editorial.notes, "updated_at": editorial.updated_at})


class SampleRunView(APIView):
    def post(self, request, slug):
        problem = get_object_or_404(Problem, slug=slug)
        incoming = SubmitSerializer(data=request.data)
        incoming.is_valid(raise_exception=True)
        outcome = run_source(
            incoming.validated_data["source_code"],
            problem.tests.filter(is_sample=True),
            problem.time_limit_ms,
            samples_only=True,
        )
        outcome["stored"] = False
        return Response(outcome)


class SubmitView(APIView):
    def post(self, request, slug):
        problem = get_object_or_404(Problem, slug=slug)
        incoming = SubmitSerializer(data=request.data)
        incoming.is_valid(raise_exception=True)
        source_code = incoming.validated_data["source_code"]
        outcome = run_source(source_code, problem.tests.all(), problem.time_limit_ms)
        submission = Submission.objects.create(
            owner=request.user,
            problem=problem,
            source_code=source_code,
            verdict=outcome["verdict"],
            runtime_ms=outcome["runtime_ms"],
            message=outcome["message"],
        )
        return Response(SubmissionSerializer(submission).data, status=201)


class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        queryset = Submission.objects.filter(owner=self.request.user).select_related("problem")
        slug = self.request.query_params.get("problem")
        if slug:
            queryset = queryset.filter(problem__slug=slug)
        return queryset


class SubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(owner=self.request.user).select_related("problem")


class SubmissionCompareView(APIView):
    def get(self, request):
        left_id = _submission_id(request.query_params.get("left"))
        right_id = _submission_id(request.query_params.get("right"))
        if left_id is None or right_id is None:
            return Response(
                {"detail": "Provide integer left and right submission ids."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        owned = Submission.objects.filter(owner=request.user).select_related("problem")
        left = get_object_or_404(owned, pk=left_id)
        right = get_object_or_404(owned, pk=right_id)
        return Response(
            {
                "left": SubmissionSerializer(left).data,
                "right": SubmissionSerializer(right).data,
                "same_verdict": left.verdict == right.verdict,
                "same_source": left.source_code == right.source_code,
                "runtime_delta_ms": right.runtime_ms - left.runtime_ms,
                "source_diff": _source_diff(left, right),
            }
        )


def _submission_id(raw):
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _source_diff(left: Submission, right: Submission) -> str:
    diff = difflib.unified_diff(
        left.source_code.splitlines(),
        right.source_code.splitlines(),
        fromfile=f"submission-{left.pk}.py",
        tofile=f"submission-{right.pk}.py",
        lineterm="",
    )
    return "\n".join(diff)
