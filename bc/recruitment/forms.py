from django import forms


class SearchAlertSubscriptionForm(forms.Form):
    email = forms.EmailField()
    email.widget.attrs.update({"autocomplete": "off", "autocapitalize": "off"})
