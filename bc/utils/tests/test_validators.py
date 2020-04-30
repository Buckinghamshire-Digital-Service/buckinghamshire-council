from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..validators import FileExtensionValidator, validate_youtube_domain


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


class FileExtensionValidatorTest(TestCase):
    def test_trivial_validator_objects_to_everything(self):
        validate_file_extension = FileExtensionValidator()
        self.assertEqual(validate_file_extension.valid_extensions, [])
        for file_name in [
            "hello_world.txt",
            "abc.jpg",
            ".secrets",
            "test",
            "C:\\Users\\FluffyLump\\Letter to Grandma.doc",
            "C:/Users/FluffyLump/Letter to Grandma.doc",
            "/var/lib/nginx/important_server_records.log",
        ]:
            with self.subTest(file_name=file_name):
                with self.assertRaises(ValidationError):
                    validate_file_extension(SimpleUploadedFile(file_name, b"1"))

    def test_valid_file_extensions_are_validated(self):
        valid_extensions = [".jpg"]
        validate_file_extension = FileExtensionValidator(valid_extensions)
        self.assertEqual(validate_file_extension.valid_extensions, valid_extensions)
        for file_name in [
            "hello_world.jpg",
            "abc.jpg",
            ".secrets.jpg",
            "test.multiple.extensions.jpg",
            "C:\\Users\\FluffyLump\\Letter to Grandma.jpg",
            "C:/Users/FluffyLump/Letter to Grandma.jpg",
            "/var/lib/nginx/important_server_records.jpg",
        ]:
            with self.subTest(file_name=file_name):
                try:
                    validate_file_extension(SimpleUploadedFile(file_name, b"1"))
                except ValidationError:
                    self.fail(f"{file_name} was unexpectedly found invalid")

    def test_invalid_file_extensions_are_not_validated(self):
        valid_extensions = [".jpg"]
        validate_file_extension = FileExtensionValidator(valid_extensions)
        self.assertEqual(validate_file_extension.valid_extensions, valid_extensions)
        for file_name in [
            "hello_world.txt",
            ".secrets",
            "test",
            "C:\\Users\\FluffyLump\\Letter to Grandma.doc",
            "C:/Users/FluffyLump/Letter to Grandma.doc",
            "/var/lib/nginx/important_server_records.log",
        ]:
            with self.subTest(file_name=file_name):
                with self.assertRaises(ValidationError):
                    validate_file_extension(SimpleUploadedFile(file_name, b"1"))

    def test_multiple_valid_file_extensions_can_be_checked(self):
        valid_extensions = [".jpg", ".png"]
        validate_file_extension = FileExtensionValidator(valid_extensions)
        self.assertEqual(validate_file_extension.valid_extensions, valid_extensions)
        for file_name in [
            "hello_world.png",
            "abc.jpg",
            ".secrets.jpg",
            "test.multiple.extensions.png.jpg",
            "C:\\Users\\FluffyLump\\Letter to Grandma.png",
            "C:/Users/FluffyLump/Letter to Grandma.jpg",
            "/var/lib/nginx/important_server_records.png",
        ]:
            with self.subTest(file_name=file_name):
                try:
                    validate_file_extension(SimpleUploadedFile(file_name, b"1"))
                except ValidationError:
                    self.fail(f"{file_name} was unexpectedly found invalid")
