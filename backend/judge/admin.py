from django.contrib import admin

from .models import Hint, Problem, ProblemTest, Submission, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("label", "slug")
    search_fields = ("label", "slug")


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "slug", "difficulty", "time_limit_ms")
    list_filter = ("difficulty", "tags")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    ordering = ("position",)


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ("problem", "position")
    ordering = ("problem", "position")
    search_fields = ("body", "problem__slug")


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
