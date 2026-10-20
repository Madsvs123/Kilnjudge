from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Problem, Submission
from .runner import run_source
from .serializers import (
    ProblemDetailSerializer,
    ProblemListSerializer,
    RegisterSerializer,
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
    return Problem.objects.prefetch_related("tags", "hints").annotate(
        sample_count=Count("tests", filter=Q(tests__is_sample=True)),
        hidden_count=Count("tests", filter=Q(tests__is_sample=False)),
    )


class ProblemListView(generics.ListAPIView):
    serializer_class = ProblemListSerializer

    def get_queryset(self):
        return _annotated_problems()


class ProblemDetailView(generics.RetrieveAPIView):
    serializer_class = ProblemDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return _annotated_problems()


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
