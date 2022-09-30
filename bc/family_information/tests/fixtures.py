import factory
import wagtail_factories

from bc.family_information import models


class SubsiteHomePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.SubsiteHomePage

    title = factory.Sequence(lambda n: f"Subsite Home Page {n}")

    banner_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")
    banner_title = "Banner title"
    banner_description = "Banner description"
    banner_link = "https://example.com"

    hero_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")


class CategoryTypeOnePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.CategoryTypeOnePage

    title = factory.Sequence(lambda n: f"Category Type One Page {n}")

    banner_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")
    banner_title = "Banner title"
    banner_description = "Banner description"
    banner_link = "https://example.com"
