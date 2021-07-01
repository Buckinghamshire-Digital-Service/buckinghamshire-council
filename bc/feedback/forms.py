from django import forms

from bc.feedback.models import FeedbackComment, UsefulnessFeedback


class UsefulnessFeedbackForm(forms.ModelForm):
    class Meta:
        model = UsefulnessFeedback
        fields = ("page", "useful")
        # The basic yes/no form are always prefilled and do not require the user to fill
        # any form. The user only submits one of the two forms (one prefilled with
        # useful=False, the other with useful=True).
        widgets = {
            "page": forms.HiddenInput(),
            "useful": forms.HiddenInput(),
        }


class FeedbackCommentForm(forms.ModelForm):
    class Meta:
        model = FeedbackComment
        fields = ("page", "action", "issue")
        widgets = {
            "page": forms.HiddenInput(),
        }
