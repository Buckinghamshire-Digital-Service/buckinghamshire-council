import factory
import wagtail_factories

from bc.family_information import models


class SubsiteHomePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.SubsiteHomePage

    title = factory.Sequence(lambda n: f"Familiy Information Service Home Page {n}")
    listing_summary = "Familiy Information Service Home Page"

    banner_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")
    banner_title = "Banner title"
    banner_description = "Banner description"
    banner_link = "https://example.com"
    banner_link_text = "Banner link text"

    hero_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")


class CategoryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.CategoryPage

    title = factory.Sequence(lambda n: f"Category Type One Page {n}")
    listing_summary = "Category Type One Page"

    banner_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")
    banner_title = "Banner title"
    banner_description = "Banner description"
    banner_link = "https://example.com"
    banner_link_text = "Banner link text"
