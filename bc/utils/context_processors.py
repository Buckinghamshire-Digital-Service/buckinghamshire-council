from django.conf import settings


def global_vars(request):
    return {
        "GOOGLE_TAG_MANAGER_ID": getattr(settings, "GOOGLE_TAG_MANAGER_ID", None),
        "GOOGLE_TAG_MANAGER_AUTH": getattr(settings, "GOOGLE_TAG_MANAGER_AUTH", None),
        "GOOGLE_TAG_MANAGER_ENV_ID": getattr(
            settings, "GOOGLE_TAG_MANAGER_ENV_ID", None
        ),
        "YANDEX_VERIFICATION_STRING": getattr(
            settings, "YANDEX_VERIFICATION_STRING", None
        ),
        "FATHOM_SITE_ID": getattr(settings, "FATHOM_SITE_ID", None),
    }
