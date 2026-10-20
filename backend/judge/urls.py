from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    MeView,
    ProblemDetailView,
    ProblemListView,
    RegisterView,
    SubmissionDetailView,
    SubmissionListView,
    SubmitView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("problems/", ProblemListView.as_view(), name="problem-list"),
    path("problems/<slug:slug>/", ProblemDetailView.as_view(), name="problem-detail"),
    path("problems/<slug:slug>/submit/", SubmitView.as_view(), name="submit"),
    path("submissions/", SubmissionListView.as_view(), name="submission-list"),
    path("submissions/<int:pk>/", SubmissionDetailView.as_view(), name="submission-detail"),
]
