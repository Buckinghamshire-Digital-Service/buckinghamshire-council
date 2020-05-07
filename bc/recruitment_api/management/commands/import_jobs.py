from django.core.management.base import BaseCommand
from django.utils.timezone import now

from bc.images.models import CustomImage, import_image_from_url
from bc.recruitment.models import RecruitmentHomePage, TalentLinkJob
from bc.recruitment_api.client import get_client
from bc.recruitment_api.utils import (
    delete_jobs,
    import_attachments_for_job,
    update_job_from_ad,
)


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
        # We import jobs for each Recruitment Homepage, including draft ones
        # so it is possible to import jobs before going live.
        if not RecruitmentHomePage.objects.exists():
            msg = f"Please create a RecruitmentHomePage page before running the import."
            self.stdout.write(self.style.ERROR(msg))

        for homepage in RecruitmentHomePage.objects.all():
            self.stdout.write(
                f"Starting import for recruitment site with homepage id {homepage.id}:"
            )
            job_board = homepage.job_board

            try:
                client = get_client(job_board=job_board)
            except AttributeError as exception:
                msg = exception.args[0] + "\n"
                msg += f"Error fetching jobs for '{homepage.job_board}' job board. Skipping import for this site."
                self.stdout.write(self.style.ERROR(msg))
                continue

            page = 1
            results = True
            num_updated = 0
            num_created = 0
            doc_imported = 0
            image_imported = 0
            errors = []
            import_timestamp = now()
            while results:
                self.stdout.write(f"Fetching page {page} from job board '{job_board}'")
                response = client.service.getAdvertisementsByPage(
                    pageNumber=page, showJobLocation=True
                )
                results = response["advertisements"]
                page += 1
                if results:
                    self.stdout.write(f"{len(results['advertisement'])} advertisements")
                    for ad in response["advertisements"]["advertisement"]:
                        try:
                            job = TalentLinkJob.objects.get(talentlink_id=ad["id"])
                            created = False
                        except TalentLinkJob.DoesNotExist:
                            job = TalentLinkJob(
                                talentlink_id=ad["id"], homepage=homepage
                            )
                            created = True
                        try:
                            job = update_job_from_ad(
                                job,
                                ad,
                                homepage=homepage,
                                defaults={"last_imported": import_timestamp},
                                import_categories=options["import_categories"],
                            )
                        except Exception as e:
                            msg = (
                                f"Error occurred while processing job {ad['id']} {ad['jobNumber']}:\n"
                                + str(e)
                            )
                            errors.append(msg)
                        else:
                            if created:
                                num_created += 1
                            else:
                                num_updated += 1

                            # Fetch attachments via a different call
                            try:
                                doc_imported += import_attachments_for_job(job, client)
                            except Exception as e:
                                msg = (
                                    "Error occurred while importing attachments "
                                    + f"for job {ad['id']} {ad['jobNumber']}:\n"
                                    + str(e)
                                )
                                errors.append(msg)

                            # Fetch logo image via a different call
                            image_found = False
                            try:
                                # This will return a assignedImageDto object with
                                #   'id', 'url', 'position'
                                logo_response = client.service.getAdvertisementImages(
                                    job.talentlink_id
                                )
                                for image in logo_response:
                                    if image["position"] == "Logo":
                                        talentlink_image_id = image["id"]

                                        # Only update image if it is changed or new
                                        try:
                                            logo_image = CustomImage.objects.get(
                                                talentlink_image_id=talentlink_image_id
                                            )
                                        except CustomImage.DoesNotExist:
                                            logo_image = import_image_from_url(
                                                title=job.title,
                                                url=image["url"],
                                                filename="logo "
                                                + str(job.talentlink_id),
                                                talentlink_image_id=talentlink_image_id,
                                                collection_name="jobs_logo",
                                            )
                                            image_imported += 1
                                        finally:
                                            job.logo = logo_image
                                            job.save()
                                            image_found = True
                                            break
                            except Exception as e:
                                msg = (
                                    f"Error occurred while importing logo image for job {ad['id']} {ad['jobNumber']}:\n"
                                    + str(e)
                                )
                                errors.append(msg)

                            # Remove logo from existing job if it is gone from this import
                            if (not created) and (not image_found) and job.logo:
                                # Also delete logo image if not used anywhere else too
                                if (
                                    TalentLinkJob.objects.filter(logo=job.logo).count()
                                    == 1
                                ):
                                    job.logo.delete()
                                job.logo = None
                                job.save()

            # Check for outdated jobs
            num_deleted = 0
            try:
                num_deleted = delete_jobs(
                    imported_before=import_timestamp, homepage=homepage
                )
            except Exception as e:
                msg = f"Error occurred while deleting jobs:\n" + str(e)
                errors.append(msg)

            self.stdout.write("No more results")
            self.stdout.write(f"{num_updated} existing jobs updated")
            self.stdout.write(f"{num_created} new jobs created")
            self.stdout.write(f"{doc_imported} new documents imported")
            self.stdout.write(f"{image_imported} new images imported")
            self.stdout.write(f"{num_deleted} jobs deleted")
            self.stdout.write(self.style.ERROR(f"{len(errors)} errors"))
            for msg in errors:
                self.stdout.write(self.style.ERROR(msg))
