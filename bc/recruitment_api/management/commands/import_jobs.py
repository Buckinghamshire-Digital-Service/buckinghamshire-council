from django.core.management.base import BaseCommand
from django.utils.timezone import now

from bc.recruitment.models import TalentLinkJob
from bc.recruitment_api.client import get_client
from bc.recruitment_api.utils import update_job_from_ad


class Command(BaseCommand):
    help = "Imports all jobs from the API"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--import_categories",
            action="store_true",
            help="Import missing categories instead of rejecting jobs without matching categories.",
        )

    def handle(self, *args, **options):
        client = get_client()
        page = 1
        results = True
        num_updated = 0
        num_created = 0
        errors = []
        while results:
            self.stdout.write(f"Fetching page {page}")
            response = client.service.getAdvertisementsByPage(page)
            results = response["advertisements"]
            page += 1
            if results:
                self.stdout.write(f"{len(results['advertisement'])} advertisements")
                for ad in response["advertisements"]["advertisement"]:

                    try:
                        job = TalentLinkJob.objects.get(talentlink_id=ad["id"])
                        created = False
                    except TalentLinkJob.DoesNotExist:
                        job = TalentLinkJob(talentlink_id=ad["id"])
                        created = True

                    try:
                        job = update_job_from_ad(
                            job,
                            ad,
                            defaults={"last_imported": now()},
                            import_categories=options["import_categories"],
                        )
                    except Exception as e:
                        msg = (
                            f"Error occurred while processing job {ad['id']}:\n"
                            + str(e)
                        )
                        errors.append(msg)
                    else:
                        if created:
                            num_created += 1
                        else:
                            num_updated += 1

        self.stdout.write("No more results")
        self.stdout.write(f"{num_updated} existing jobs updated")
        self.stdout.write(f"{num_created} new jobs created")
        self.stdout.write(self.style.ERROR(f"{len(errors)} errors"))
        for error in errors:
            self.stdout.write(self.style.ERROR(msg))
