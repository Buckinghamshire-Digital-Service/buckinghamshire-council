from wagtail.admin.filters import DateRangePickerWidget

import django_filters

from bc.feedback.models import FeedbackComment


class FeedbackCommentFilterSet(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter(
        widget=DateRangePickerWidget(),
    )

    class Meta:
        model = FeedbackComment
        fields = ["created"]
