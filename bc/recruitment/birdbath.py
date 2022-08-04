from birdbath.processors import BaseModelDeleter

from bc.recruitment.models import JobAlertSubscription


class DeleteAllRecruitmentAlertSubscriptionProcessor(BaseModelDeleter):
    """Deletes all RecruitmentAlertSubscription records."""

    model = JobAlertSubscription
