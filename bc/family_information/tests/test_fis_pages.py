from wagtail.test.utils import WagtailPageTestCase

from bc.family_information.models import SubsiteHomePage
from bc.standardpages.models import InformationPage


class TestFISHomePage(WagtailPageTestCase):
    def test_can_create_infopage_at_fis_homepage(self):
        """
        Test information pages can be created under the FIS homepage.

        This is only a regression test. From the current status of the staging
        server, it used to be possible to create InformationPage under
        SubsiteHomePage. At some point this has been prevented
        accidentally, making another update necessary to fix this.

        This test is added to prevent the accidental change in the future. If
        it becomes a deliberate decision to prevent the creation, this test
        should be updated to `assertCanNotCreateAt`.

        See also: https://docs.wagtail.org/en/stable/advanced_topics/testing.html#wagtail.test.utils.WagtailPageTestCase.assertCanNotCreateAt  # noqa: E501
        """
        self.assertCanCreateAt(SubsiteHomePage, InformationPage)
