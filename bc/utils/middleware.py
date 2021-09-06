from django.middleware.csrf import CsrfViewMiddleware

from wagtail.core.models import Page
from wagtail.core.views import serve

from bc.cases.models import ApteanRespondCaseFormPage
from bc.forms.models import FormPage


class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    """A middleware class to exempt pages of certain types from CSRF checks.

    For Wagtail pages, decorating the 'view' function is not possible, as all are served
    with `wagtail.core.views.serve`.

    The pages' `.serve()` method can be decorated in some cases where a decorator acts
    on the return value of the 'view' function. However the `@csrf_exempt` decorator
    adds an attribute to the view function itself.

    Ref https://github.com/wagtail/wagtail/issues/3066 for discussion and the source of
    the code below.
    """

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
