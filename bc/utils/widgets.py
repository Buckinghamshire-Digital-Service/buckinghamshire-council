from django import forms


class CustomCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    template_name = (
        "patterns/molecules/form-widgets/custom_checkbox_select_multiple.html"
    )


class CustomCheckboxSelectSingle(forms.widgets.CheckboxInput):
    template_name = "patterns/molecules/form-widgets/custom_checkbox_select_single.html"


class TelephoneNumberInput(forms.widgets.TextInput):
    input_type = "tel"

    def __init__(self, attrs=None):
        default_attrs = {"autocomplete": "tel"}
        if attrs:
            default_attrs.update(attrs)
        return super().__init__(default_attrs)
