from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns

from wagtail_transfer import urls as wagtailtransfer_urls

from bc.area_finder import urls as area_finder_urls
from bc.feedback import urls as feedback_urls
from bc.search.views import JobAlertConfirmView, JobAlertUnsubscribeView, SearchView
from bc.utils.cache import get_default_cache_control_decorator

# Private URLs are not meant to be cached.
private_urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("feedback/", include(feedback_urls, namespace="feedback")),
    # Search cache-control headers are set on the view itself.
    path("search/", SearchView.as_view(), name="search"),
    path("api/v2/area-finder/", include(area_finder_urls)),
    path(
        "confirm_job_alert/<str:token>/",
        JobAlertConfirmView.as_view(),
        name="confirm_job_alert",
    ),
    path(
        "unsubscribe_job_alert/<str:token>/",
        JobAlertUnsubscribeView.as_view(),
        name="unsubscribe_job_alert",
    ),
    re_path(r"^wagtail-transfer/", include(wagtailtransfer_urls)),
]


# Public URLs that are meant to be cached.
urlpatterns = [path("sitemap.xml", sitemap)]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # Add views for testing 404 and 500 templates
        path(
            "test404/",
            TemplateView.as_view(template_name="patterns/pages/errors/404.html"),
        ),
        path(
            "test500/",
            TemplateView.as_view(template_name="patterns/pages/errors/500.html"),
        ),
    ]

    # Try to install the django debug toolbar, if exists
    if apps.is_installed("debug_toolbar"):
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


# Style guide
if getattr(settings, "PATTERN_LIBRARY_ENABLED", False) and apps.is_installed(
    "pattern_library"
):
    private_urlpatterns += [path("pattern-library/", include("pattern_library.urls"))]


# Set public URLs to use the "default" cache settings.
urlpatterns = decorate_urlpatterns(urlpatterns, get_default_cache_control_decorator())

# Set vary header to instruct cache to serve different version on different
# cookies, different request method (e.g. AJAX) and different protocol
# (http vs https).
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers(
        "Cookie", "X-Requested-With", "X-Forwarded-Proto", "Accept-Encoding"
    ),
)

# Join private and public URLs.
urlpatterns = (
    private_urlpatterns
    + urlpatterns
    + [
        # Add Wagtail URLs at the end.
        # Wagtail cache-control is set on the page models's serve methods.
        path("", include(wagtail_urls))
    ]
)

# Error handlers
handler404 = "bc.utils.views.page_not_found"
handler500 = "bc.utils.views.server_error"
