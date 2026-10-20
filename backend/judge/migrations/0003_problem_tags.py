from django.db import migrations, models


def forwards(apps, schema_editor):
    from judge.catalog import load_catalog

    load_catalog(
        apps.get_model("judge", "Problem"),
        apps.get_model("judge", "ProblemTest"),
        tag_model=apps.get_model("judge", "Tag"),
    )


def backwards(apps, schema_editor):
    apps.get_model("judge", "Tag").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("judge", "0002_seed_catalog"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("slug", models.SlugField(max_length=40, unique=True)),
                ("label", models.CharField(max_length=40)),
            ],
            options={
                "ordering": ["label", "slug"],
            },
        ),
        migrations.AddField(
            model_name="problem",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="problems", to="judge.tag"),
        ),
        migrations.RunPython(forwards, backwards),
    ]
