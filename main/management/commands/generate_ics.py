import os

from django.core.management.base import BaseCommand

from main import models, utils


class Command(BaseCommand):
    help = "Generate ICS event file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--workshop",
            type=int,
            help="Choose workshop ID to create ICS event for.",
        )

    def handle(self, *args, **options):
        workshops = {}
        for workshop in models.Workshop.objects.filter(scheduled_at__isnull=False):
            workshops[workshop.id] = workshop.title
            print(f"{workshop.id}: {workshop.title}")

        if options["workshop"]:
            workshop_id = options["workshop"]
            workshop = models.Workshop.objects.get(id=workshop_id)
        else:
            self.stdout.write(self.style.NOTICE("Choose a workshop:"))
            workshop_response = int(input())
            workshop = models.Workshop.objects.get(title=workshops[workshop_response])

        self.stdout.write(self.style.SUCCESS(f"Workshop selected: {workshop.title}"))
        ics = utils.get_ics(workshop)
        with open(f"{workshop.slug}.ics", "w") as f:
            f.write(ics)

        self.stdout.write(
            self.style.SUCCESS(f"ICS file saved at {os.getcwd()}/{workshop.slug}.ics")
        )
