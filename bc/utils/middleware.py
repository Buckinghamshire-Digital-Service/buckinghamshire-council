from django.middleware.csrf import CsrfViewMiddleware

from wagtail.core.models import Page
from wagtail.core.views import serve

from bc.cases.models import ApteanRespondCaseFormPage
from bc.forms.models import FormPage


class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):

        if callback == serve:
            # We are visiting a Wagtail page.
            # Bypass CSRF validation for FormPages and ApteanRespondCaseFormPages.
            path = callback_args[0]
            if any(
                path.startswith(page.get_url_parts()[-1][1:])
                for page in Page.objects.type(FormPage, ApteanRespondCaseFormPage).only(
                    "url_path"
                )
            ):
                return None

        return super().process_view(request, callback, callback_args, callback_kwargs)
