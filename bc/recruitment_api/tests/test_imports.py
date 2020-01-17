from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from .fixtures import TalentLinkJobFactory, advertisement, no_further_pages_response


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class ImportTest(TestCase):
    def get_mocked_client(self):
        client = mock.Mock()
        client.service.getAdvertisementsByPage.side_effect = [
            {"advertisements": {"advertisement": [advertisement]}, "totalResults": 143},
            no_further_pages_response,
        ]
        return client

    def test_with_mocked_client(self, mock_get_client):

        mock_get_client.return_value = self.get_mocked_client()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("1 new jobs created", output)

    def test_with_existing_job(self, mock_get_client):
        TalentLinkJobFactory(talentlink_id=164579)

        mock_get_client.return_value = self.get_mocked_client()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("1 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)
