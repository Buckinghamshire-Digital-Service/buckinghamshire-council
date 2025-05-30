from django import forms

from wagtail.admin.filters import DateRangePickerWidget

import django_filters

from bc.feedback.models import FeedbackComment, UsefulnessFeedback


class FeedbackCommentFilterSet(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter(
        widget=DateRangePickerWidget,
    )

    class Meta:
        model = FeedbackComment
        fields = ["created"]


class UsefulnessFeedbackFilterSet(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter(
        widget=DateRangePickerWidget,
    )

    useful = django_filters.ChoiceFilter(
        label="Useful",
        choices=((True, "Yes"), (False, "No")),
        empty_label="All",
        widget=forms.RadioSelect,
    )

    class Meta:
        model = UsefulnessFeedback
        fields = ["created", "useful"]
