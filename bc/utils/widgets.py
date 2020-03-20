from django import forms
from django.forms.widgets import Widget


class CustomCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    template_name = (
        "patterns/molecules/form-widgets/custom_checkbox_select_multiple.html"
    )


class CustomHeadingField(Widget):
    template_name = "patterns/molecules/form-widgets/heading.html"


class CustomSubheadingField(Widget):
    template_name = "patterns/molecules/form-widgets/subheading.html"
