from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load JSON fixtures bundled with the judge app."

    def add_arguments(self, parser):
        parser.add_argument(
            "labels",
            nargs="*",
            help="Fixture names inside judge/fixtures. Defaults to every JSON file there.",
        )

    def handle(self, *args, **options):
        fixture_dir = Path(__file__).resolve().parents[2] / "fixtures"
        labels = options["labels"]
        if labels:
            paths = []
            for label in labels:
                name = label if str(label).endswith(".json") else f"{label}.json"
                path = fixture_dir / name
                if not path.is_file():
                    raise CommandError(f"No fixture named {name}.")
                paths.append(path)
        else:
            paths = sorted(fixture_dir.glob("*.json"))
        if not paths:
            raise CommandError(f"No JSON fixtures in {fixture_dir}.")
        for path in paths:
            call_command("loaddata", str(path), verbosity=options["verbosity"])
            self.stdout.write(self.style.SUCCESS(f"Loaded {path.name}."))
