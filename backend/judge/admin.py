from django.contrib import admin

from .models import Problem, ProblemTest, Submission


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "slug", "difficulty", "time_limit_ms")
    list_filter = ("difficulty",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("position",)


@admin.register(ProblemTest)
class ProblemTestAdmin(admin.ModelAdmin):
    list_display = ("problem", "position", "is_sample")
    list_filter = ("is_sample", "problem")
    ordering = ("problem", "position")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "owner", "problem", "verdict", "runtime_ms")
    list_filter = ("verdict", "problem")
    search_fields = ("owner__username", "problem__title")
    readonly_fields = ("created_at",)
