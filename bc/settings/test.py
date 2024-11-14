from .base import *  # noqa

SECRET_KEY = "fake_secret_key_to_run_tests"

RECAPTCHA_PUBLIC_KEY = "dummy_public_key"
RECAPTCHA_PRIVATE_KEY = "dummy_private_key"  # pragma: allowlist secret

RESPOND_COMPLAINTS_WEBSERVICE = "TestCreateComplaints"
RESPOND_FOI_WEBSERVICE = "TestCreateFOI"
RESPOND_SAR_WEBSERVICE = "TestCreateSAR"
RESPOND_COMMENTS_WEBSERVICE = "TestCreateComments"
RESPOND_COMPLIMENTS_WEBSERVICE = "TestCreateCompliments"
RESPOND_DISCLOSURES_WEBSERVICE = "TestCreateDisclosures"

SECURE_SSL_REDIRECT = False

WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.database"}}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "database_cache",
    }
}

# Ignore proxy count in tests
XFF_ALWAYS_PROXY = False
