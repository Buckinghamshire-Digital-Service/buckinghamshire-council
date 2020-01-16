from django.core.management.base import BaseCommand

from bc.recruitment.models import TalentLinkJob
from bc.recruitment_api.client import get_client
from bc.recruitment_api.utils import update_job_from_ad


class Command(BaseCommand):
    help = "Imports all jobs from the API"

    def handle(self, *args, **options):
        client = get_client()
        page = 1
        results = True
        updated = 0
        created = 0
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
                        updated += 1
                    except TalentLinkJob.DoesNotExist:
                        job = TalentLinkJob(talentlink_id=ad["id"])
                        created += 1

                    job = update_job_from_ad(job, ad)
        self.stdout.write(f"{updated} existing jobs updated")
        self.stdout.write(f"{created} new jobs created")
