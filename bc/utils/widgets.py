from django import forms


class CustomCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    template_name = (
        "patterns/molecules/form-widgets/custom_checkbox_select_multiple.html"
    )


class CustomCheckboxSelectSingle(forms.widgets.CheckboxInput):
    template_name = "patterns/molecules/form-widgets/custom_checkbox_select_single.html"
