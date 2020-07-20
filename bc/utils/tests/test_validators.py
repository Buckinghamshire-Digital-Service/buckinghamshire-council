from django.core.exceptions import ValidationError
from django.test import TestCase

from ..validators import validate_linkedin_domain, validate_youtube_domain


class YouTubeURLValidatorTest(TestCase):
    def test_valid_values_are_validated(self):
        values = [
            "http://www.youtube.com/",
            "http://youtu.be/",
            "https://www.youtube.com/",
            "https://youtu.be/",
            "http://www.youtube.com/bc",
            "http://www.youtube.com/bc/",
            "https://www.youtube.com/bc",
            "https://www.youtube.com/bc/",
            "https://www.youtube.com/c/bc",
            "https://www.youtube.com/c/bc/",
        ]
        for value in values:
            with self.subTest(url=value):
                validate_youtube_domain(value)

    def test_invalid_values_are_not_validated(self):
        values = ["https://youtube.com/", "https://www.youtube.org/"]
        for value in values:
            with self.subTest(url=value):
                with self.assertRaises(ValidationError):
                    validate_youtube_domain(value)


class LinkedInURLValidatorTest(TestCase):
    def test_valid_values_are_validated(self):
        values = [
            "http://www.linkedin.com/",
            "https://www.linkedin.com/",
            "http://www.linkedin.com/bc",
            "http://www.linkedin.com/bc/",
            "https://www.linkedin.com/bc",
            "https://www.linkedin.com/bc/",
            "https://www.linkedin.com/c/bc",
            "https://www.linkedin.com/c/bc/",
        ]
        for value in values:
            with self.subTest(url=value):
                validate_linkedin_domain(value)

    def test_invalid_values_are_not_validated(self):
        values = ["https://linked.in/", "https://www.linkedin.org/"]
        for value in values:
            with self.subTest(url=value):
                with self.assertRaises(ValidationError):
                    validate_linkedin_domain(value)
