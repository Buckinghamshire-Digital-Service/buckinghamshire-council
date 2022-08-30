from birdbath.processors import BaseModelDeleter

from bc.blogs.models import BlogAlertSubscription


class DeleteAllBlogAlertSubscriptionProcessor(BaseModelDeleter):
    """Deletes all BlogAlertSubscription records."""

    model = BlogAlertSubscription
