from django.core.exceptions import ValidationError
from django.test import TestCase

from ..validators import validate_youtube_domain


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
