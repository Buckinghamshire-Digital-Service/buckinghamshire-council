from django import forms

from bc.feedback.models import UsefulnessFeedback


class UsefulnessFeedbackForm(forms.ModelForm):
    class Meta:
        model = UsefulnessFeedback
        fields = ("page", "useful")
