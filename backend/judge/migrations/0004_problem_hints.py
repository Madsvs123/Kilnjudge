from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    from judge.catalog import load_catalog

    load_catalog(
        apps.get_model("judge", "Problem"),
        apps.get_model("judge", "ProblemTest"),
        tag_model=apps.get_model("judge", "Tag"),
        hint_model=apps.get_model("judge", "Hint"),
    )


def backwards(apps, schema_editor):
    apps.get_model("judge", "Hint").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("judge", "0003_problem_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hint",
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
                ("position", models.PositiveIntegerField()),
                ("body", models.TextField()),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hints",
                        to="judge.problem",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
            },
        ),
        migrations.AddConstraint(
            model_name="hint",
            constraint=models.UniqueConstraint(
                fields=("problem", "position"),
                name="unique_problem_hint_position",
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]
