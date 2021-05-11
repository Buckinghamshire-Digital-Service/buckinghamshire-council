from http import HTTPStatus

from django import test, urls


class TestUsefulnessFeedbackCreateView(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_get_fails(self):
        url = urls.reverse("feedback:create_usefulness_feedback")

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
