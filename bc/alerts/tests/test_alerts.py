from django.test import TestCase

from bc.alerts.models import Alert
from bc.alerts.templatetags.alert_tags import get_alerts
from bc.home.models import HomePage
from bc.standardpages.tests.fixtures import InformationPageFactory

from .fixtures import AlertFactory


class AlertTest(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()
        self.child = InformationPageFactory.build()
        self.homepage.add_child(instance=self.child)

    def test_alert_shown_when_on_page(self):
        alert = AlertFactory(page=self.homepage, show_on=Alert.PAGE_ONLY)
        resp = self.client.get(self.homepage.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, alert.title)

    def test_non_cascading_alert_got_for_page(self):
        alert = AlertFactory(page=self.homepage, show_on=Alert.PAGE_ONLY)
        alerts = Alert.get_alerts_for_page(self.homepage)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0], alert)

    def test_non_cascading_alert_not_got_for_child_page(self):
        AlertFactory(page=self.homepage, show_on=Alert.PAGE_ONLY)
        alerts = Alert.get_alerts_for_page(self.child)
        self.assertEqual(len(alerts), 0)

    def test_cascading_alert_got_for_page(self):
        alert = AlertFactory(page=self.homepage, show_on=Alert.PAGE_AND_DESCENDANTS)
        alerts = Alert.get_alerts_for_page(self.homepage)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0], alert)

    def test_cascading_alert_got_for_child_page(self):
        alert = AlertFactory(page=self.homepage, show_on=Alert.PAGE_AND_DESCENDANTS)
        alerts = Alert.get_alerts_for_page(self.child)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0], alert)

    def test_alerts_are_fetched_in_tree_order(self):
        child_alert = AlertFactory(page=self.child)
        homepage_alert = AlertFactory(
            page=self.homepage, show_on=Alert.PAGE_AND_DESCENDANTS
        )
        alerts = Alert.get_alerts_for_page(self.child)
        self.assertEqual(len(alerts), 2)
        self.assertEqual(alerts[0], homepage_alert)
        self.assertEqual(alerts[1], child_alert)

    def test_template_tag_works_for_pages(self):
        try:
            get_alerts(self.homepage)
        except Exception:
            self.fail("get_alerts tag raised an error unexpectedly")

    def test_template_tag_works_for_non_page_requests(self):
        for page_arg in ["abc", None, {"foo": "bar"}]:
            with self.subTest(page_arg=page_arg):
                try:
                    get_alerts(page_arg)
                except Exception:
                    self.fail("get_alerts tag raised an error unexpectedly")
