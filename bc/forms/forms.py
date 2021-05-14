from django.core.exceptions import ValidationError

from wagtail.admin.forms import WagtailAdminPageForm


class LookupPageForm(WagtailAdminPageForm):
    def clean(self):
        super().clean()
        formset = self.formsets["responses"]

        seen_values = set()
        duplicates = set()
        for form in formset.forms:
            form.is_valid()
            if (
                "postcodes" in form.errors
                or formset._should_delete_form(form)
                or "postcodes" not in form.cleaned_data
            ):
                continue

            duplicates = duplicates | seen_values & set(form.cleaned_data["postcodes"])
            seen_values = seen_values | set(form.cleaned_data["postcodes"])

        if duplicates:
            if len(duplicates) > 1:
                message = f"The postcodes {', '.join(duplicates)} appear in multiple responses"
            else:
                message = f"The postcode {', '.join(duplicates)} appears in multiple responses"
            raise ValidationError(message)
