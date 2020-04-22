import datetime
import json

import factory


class JobCategoryFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Job Category {n}")
    description = factory.Faker("sentence", nb_words=10)

    class Meta:
        model = "recruitment.JobCategory"


class JobSubcategoryFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Job Subcategory {n}")

    class Meta:
        model = "recruitment.JobSubcategory"


class RecruitmentHomePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "recruitment.RecruitmentHomePage"

    title = factory.Sequence(lambda n: f"Recruitment HomePage")
    hero_title = "foo"
    hero_link_text = "foo"
    search_box_placeholder = "foo"


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

    searchable_salary = factory.Faker("sentence", nb_words=2)
    location = factory.Faker("city")
    posting_start_date = factory.Faker(
        "date_time_this_month", tzinfo=datetime.timezone.utc
    )
    posting_end_date = factory.Faker(
        "date_time_this_month", tzinfo=datetime.timezone.utc
    )


class JobAlertSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "recruitment.JobAlertSubscription"

    search = json.dumps({})
    email = factory.Faker("email")
    confirmed = True
