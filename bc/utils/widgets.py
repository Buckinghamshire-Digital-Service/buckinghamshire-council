from django import forms
from django.templatetags.static import static

from wagtail.core.telepath import register
from wagtail.core.widget_adapters import WidgetAdapter


class BaseChartInput(forms.HiddenInput):
    def __init__(self, table_options=None, attrs=None):
        self.table_options = table_options
        super().__init__(attrs=attrs)
        self.table_options["language"] = "en-us"


class BarChartInput(BaseChartInput):
    chart_type = "Bar chart"


class PieChartInput(BaseChartInput):
    chart_type = "Pie chart"

    def __init__(self, table_options=None, attrs=None):
        super().__init__(table_options=table_options, attrs=attrs)
        self.table_options["startCols"] = 2
        self.table_options["maxCols"] = 2
        self.table_options["allowInsertColumn"] = False
        self.table_options["allowRemoveColumn"] = False


class LineChartInput(BaseChartInput):
    chart_type = "Line graph"


class ChartInputAdapter(WidgetAdapter):
    # This attribute is not strictly a Python path, but a namespace to look up a
    # matching JS constructor within Telepath. The JS constructor is registered in
    # bc/static_src/javascript/bc_admin_ui.js
    js_constructor = "bc.utils.widgets.ChartInput"

    class Media:
        js = [static("js/bc_admin_ui.js")]
        css = {"all": [static("bc_admin_ui/editor.css")]}

    def js_args(self, widget):
        return [widget.table_options, widget.chart_type]


register(ChartInputAdapter(), BarChartInput)
register(ChartInputAdapter(), PieChartInput)
register(ChartInputAdapter(), LineChartInput)


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
