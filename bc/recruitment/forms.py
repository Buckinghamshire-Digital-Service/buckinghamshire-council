from django import forms


class SearchAlertSubscriptionForm(forms.Form):
    email = forms.EmailField()
