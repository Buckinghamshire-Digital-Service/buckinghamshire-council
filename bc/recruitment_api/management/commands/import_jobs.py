from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from bc.documents.models import CustomDocument
from bc.images.models import CustomImage
from bc.recruitment.models import TalentLinkJob
from bc.recruitment_api.client import get_client
from bc.recruitment_api.utils import delete_jobs, update_job_from_ad


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
        doc_imported = 0
        image_imported = 0
        errors = []
        import_timestamp = now()
        while results:
            self.stdout.write(f"Fetching page {page}")
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
                        job = TalentLinkJob(talentlink_id=ad["id"])
                        created = True

                    try:
                        job = update_job_from_ad(
                            job,
                            ad,
                            defaults={"last_imported": import_timestamp},
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

                        # Fetch attachments via a different call
                        try:
                            # This will return list of attachments with
                            #   'content', 'description', 'fileName', 'id', 'mimeType'
                            attachments_response = client.service.getAttachments(
                                job.talentlink_id
                            )
                            for attachment in attachments_response:
                                if attachment["id"] and attachment["fileName"]:
                                    doc, created = CustomDocument.objects.get_or_create(
                                        talentlink_attachment_id=attachment["id"]
                                    )
                                    if created:
                                        doc.title = (
                                            attachment["description"]
                                            or attachment["fileName"].split(".")[0]
                                        )
                                        doc.file = ContentFile(
                                            attachment["content"],
                                            name=attachment["fileName"],
                                        )
                                        doc.save()
                                        doc_imported += 1

                                    job.attachments.add(doc)
                                    job.save()
                        except Exception as e:
                            msg = (
                                f"Error occurred while importing attachments for job {ad['id']}:\n"
                                + str(e)
                            )
                            errors.append(msg)

                        # Fetch logo image via a different call
                        image_found = False
                        try:
                            # This will return list of attachments with
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
                                        logo_image = CustomImage.import_from_url(
                                            title=job.title,
                                            url=image["url"],
                                            filename="logo " + str(job.talentlink_id),
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
                                f"Error occurred while importing logo image for job {ad['id']}:\n"
                                + str(e)
                            )
                            errors.append(msg)

                        # Remove logo from existing job if it is gone from this import
                        if (not created) and (not image_found) and job.logo:
                            job.logo = None
                            job.save()

        # Check for outdated jobs
        num_deleted = 0
        try:
            num_deleted = delete_jobs(import_timestamp)
        except Exception as e:
            msg = f"Error occurred while deleting jobs:\n" + str(e)
            errors.append(msg)

        self.stdout.write("No more results")
        self.stdout.write(f"{num_updated} existing jobs updated")
        self.stdout.write(f"{num_created} new jobs created")
        self.stdout.write(f"{doc_imported} new documents imported")
        self.stdout.write(f"{num_deleted} jobs deleted")
        self.stdout.write(self.style.ERROR(f"{len(errors)} errors"))
        for error in errors:
            self.stdout.write(self.style.ERROR(msg))
