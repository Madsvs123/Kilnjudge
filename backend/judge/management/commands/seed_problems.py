from django.core.management.base import BaseCommand

from judge.catalog import load_catalog
from judge.models import Problem, ProblemTest


class Command(BaseCommand):
    help = "Load the original Kilnjudge practice problems."

    def handle(self, *args, **options):
        load_catalog(Problem, ProblemTest)
        self.stdout.write(self.style.SUCCESS(f"Seeded {Problem.objects.count()} problems."))
