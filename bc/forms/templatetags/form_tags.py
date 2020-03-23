from django import template

register = template.Library()


@register.simple_tag
def get_form_additional_text(page, field):
    return page.form_fields.get(label=field.label).additional_text
