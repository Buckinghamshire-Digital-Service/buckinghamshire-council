from django.core.exceptions import ValidationError
from django.test import TestCase

from wagtail.core.models import Page
from wagtail.images.tests.utils import get_test_image_file
from wagtail.tests.utils import WagtailPageTests

from bc.images.models import CustomImage

from ..models import HomePage


class HomepageWagtailPageTests(WagtailPageTests):
    """
    Test page creation and infrastructure
    """

    def test_can_create_homepage(self):
        self.assertCanCreateAt(Page, HomePage)

    def test_can_only_create_homepage_under_root(self):
        self.assertAllowedParentPageTypes(
            HomePage,
            {Page},
            msg="HomePage should only be added as child of Page (root)",
        )


class HomePageModelTests(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        """
        Create a homepage which satisfies all required fields for positive test.
        Please update this when adding new require fields to the model.
        """
        self.hero_image = CustomImage.objects.create(
            title="Test image", file=get_test_image_file(),
        )
        self.homepage = HomePage(
            title="Home page",
            depth=2,
            strapline="Welcome to Buckinghamshire",
            hero_image=self.hero_image,
        )
        self.root_page.add_child(instance=self.homepage)

    def test_hero_validation_when_no_image(self):
        with self.assertRaises(ValidationError):
            self.hero_image.delete()
            self.homepage.save()

    def test_hero_validation_when_no_strapline(self):
        with self.assertRaises(ValidationError):
            self.homepage.strapline = None
            self.homepage.save()
