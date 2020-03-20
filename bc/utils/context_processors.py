from django.conf import settings


def global_vars(request):
    return {
        "GOOGLE_TAG_MANAGER_ID": getattr(settings, "GOOGLE_TAG_MANAGER_ID", None),
        "YANDEX_VERIFICATION_STRING": getattr(
            settings, "YANDEX_VERIFICATION_STRING", None
        ),
    }
