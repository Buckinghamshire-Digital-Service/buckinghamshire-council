import datetime
import json

import factory

from bc.recruitment.constants import JOB_BOARD_DEFAULT

factory.Faker._DEFAULT_LOCALE = "en_GB"


class JobCategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Job Category {n}")
    description = factory.Faker("sentence", nb_words=10)

    class Meta:
        model = "recruitment.JobCategory"


class JobSubcategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Job Subcategory {n}")

    class Meta:
        model = "recruitment.JobSubcategory"


class RecruitmentIndexPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "recruitment.RecruitmentIndexPage"

    title = factory.Sequence(lambda n: f"Recruitment IndexPage")
    listing_summary = "Recruitment IndexPage"
    hero_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")

    @classmethod
    def build_with_fk_objs_committed(cls, **kwargs):
        from bc.images.tests.fixtures import ImageFactory

        image = ImageFactory()
        return cls.build(hero_image=image, **kwargs)


class RecruitmentHomePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "recruitment.RecruitmentHomePage"

    title = factory.Sequence(lambda n: f"Recruitment HomePage")
    listing_summary = "Recruitment HomePage"
    hero_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")
    related_recruitment_index_page = factory.SubFactory(
        "bc.recruitment.tests.fixtures.RecruitmentIndexPageFactory"
    )
    hero_title = "foo"
    hero_link_text = "foo"
    search_box_placeholder = "foo"
    job_board = JOB_BOARD_DEFAULT

    @classmethod
    def build_with_fk_objs_committed(cls, **kwargs):
        from bc.images.tests.fixtures import ImageFactory

        image = ImageFactory()
        related_recruitment_index_page = RecruitmentIndexPageFactory()
        return cls.build(
            hero_image=image,
            related_recruitment_index_page=related_recruitment_index_page,
            **kwargs,
        )


class TalentLinkJobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "recruitment.TalentLinkJob"

    last_imported = factory.Faker("date_time", tzinfo=datetime.timezone.utc)

    talentlink_id = factory.Sequence(lambda n: n)
    job_number = factory.Sequence(lambda n: f"FS{str(n).zfill(5)}")

    title = factory.Faker("sentence", nb_words=5)
    subcategory = factory.SubFactory(
        "bc.recruitment.tests.fixtures.JobSubcategoryFactory"
    )
    salary_range = "£18,000 - £21,000"
    working_hours = "Full time"
    closing_date = factory.Faker("date_this_month")
    # interview dates will be a new field, not yet available in the API results
    # interview_dates = models.CharField(max_length=255)

    # postcode will be a new field, not yet available in the API results
    # postcode = models.CharField(max_length=10)
    contact_email = factory.Faker("email")

    searchable_salary = "£20,001 - £30,000"
    location_name = factory.Faker("sentence", nb_words=2)
    location_street_number = factory.Faker("building_number")
    location_street = factory.Faker("street_name")
    location_city = factory.Faker("city")
    location_region = factory.Faker("county")
    location_country = factory.Faker("random_choices", elements=["England"])
    location_postcode = factory.Faker("postcode")
    posting_start_date = factory.Faker(
        "date_time_this_month", tzinfo=datetime.timezone.utc
    )
    posting_end_date = factory.Faker(
        "date_time_this_month", tzinfo=datetime.timezone.utc
    )

    @factory.lazy_attribute
    def application_url_query(self):
        return f"jobId=ABCDEFG-{self.talentlink_id}&langCode=en_GB"


class JobAlertSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "recruitment.JobAlertSubscription"

    search = json.dumps({})
    email = factory.Faker("email")
    confirmed = True
