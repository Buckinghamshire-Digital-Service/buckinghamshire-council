import json

from django import forms


class BaseChartInput(forms.HiddenInput):
    def __init__(self, table_options=None, attrs=None):
        self.table_options = table_options
        super().__init__(attrs=attrs)
        self.table_options["language"] = "en-us"

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)

        chart_caption = ""
        chart_title = ""
        show_table_first = ""

        if value and value != "null":
            chart_caption = json.loads(value).get("chart_caption", "")
            chart_title = json.loads(value).get("chart_title", "")
            show_table_first = json.loads(value).get("show_table_first", "")

        context["widget"]["table_options_json"] = json.dumps(self.table_options)
        context["widget"]["chart_caption"] = chart_caption
        context["widget"]["chart_title"] = chart_title
        context["widget"]["show_table_first"] = show_table_first

        return context


class BarChartInput(BaseChartInput):
    template_name = "utils/widgets/bar_chart.html"

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)

        direction = ""

        if value and value != "null":
            direction = json.loads(value).get("direction", "")

        context["widget"]["direction"] = direction

        return context

class PieChartInput(BaseChartInput):
    template_name = "utils/widgets/pie_chart.html"

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)

        # direction = ""

        # if value and value != "null":
        #     direction = json.loads(value).get("direction", "")

        # context["widget"]["direction"] = direction

        return context


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
