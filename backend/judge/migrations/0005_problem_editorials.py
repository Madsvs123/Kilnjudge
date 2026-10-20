from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    from judge.catalog import load_catalog

    load_catalog(
        apps.get_model("judge", "Problem"),
        apps.get_model("judge", "ProblemTest"),
        tag_model=apps.get_model("judge", "Tag"),
        hint_model=apps.get_model("judge", "Hint"),
        editorial_model=apps.get_model("judge", "Editorial"),
    )


def backwards(apps, schema_editor):
    apps.get_model("judge", "Editorial").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("judge", "0004_problem_hints"),
    ]

    operations = [
        migrations.CreateModel(
            name="Editorial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "problem",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="editorial",
                        to="judge.problem",
                    ),
                ),
            ],
        ),
        migrations.RunPython(forwards, backwards),
    ]
