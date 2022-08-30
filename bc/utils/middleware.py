from django.middleware.csrf import CsrfViewMiddleware

from wagtail.models import Page
from wagtail.views import serve

from bc.cases.models import ApteanRespondCaseFormPage
from bc.forms.models import FormPage


class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    """A middleware class to exempt pages of certain types from CSRF checks.

    Normally this would be achieved with the `@csrf_exempt` decorator.

    For Wagtail pages the page-level equivalent 'view' function is the `.serve()`
    method. It can be decorated in some cases where a decorator acts on the return value
    of the decorated function.

    However, where a decorator acts on the function itself, such as the `@csrf_exempt`
    decorator, which adds an attribute to the function that the usual CsrfViewMiddleware
    checks for, such decoration is not possible. For Wagtail pages, the view registered
    in the URLconf and passed to CsrfViewMiddleware is always
    `wagtail.views.serve`.

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
