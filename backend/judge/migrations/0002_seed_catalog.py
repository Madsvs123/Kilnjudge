from django.db import migrations

CATALOG_SLUGS = (
    "interior-valleys",
    "square-digit-steps",
    "even-gap-twins",
    "rising-plateau-cover",
)


def forwards(apps, schema_editor):
    from judge.catalog import load_catalog

    load_catalog(apps.get_model("judge", "Problem"), apps.get_model("judge", "ProblemTest"))


def backwards(apps, schema_editor):
    problem_model = apps.get_model("judge", "Problem")
    problem_model.objects.filter(slug__in=CATALOG_SLUGS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("judge", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
