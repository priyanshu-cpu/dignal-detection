from __future__ import annotations

from django.core.management.base import BaseCommand

from detector.services import run_detection


class Command(BaseCommand):
    help = "Run the hiring and recruiting signal detection pipeline."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--source",
            action="append",
            dest="sources",
            default=[],
            help="Path or URL for an RSS/HTML source. Can be used multiple times.",
        )

    def handle(self, *args, **options) -> None:
        run = run_detection(options["sources"] or None)
        self.stdout.write(
            self.style.SUCCESS(
                f"Stored {run.signal_count} signals from {run.source_count} sources in run {run.id}."
            )
        )
