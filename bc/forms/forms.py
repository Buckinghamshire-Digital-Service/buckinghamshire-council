from django.core.exceptions import ValidationError

from wagtail.admin.forms import WagtailAdminPageForm

from bc.area_finder.utils import validate_postcode


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

            # Normalise the postcodes now. This cannot be done in the formset form
            # class. See https://github.com/wagtail/wagtail/issues/3175
            try:
                form.cleaned_data["postcodes"] = [
                    validate_postcode(postcode)
                    for postcode in form.cleaned_data["postcodes"]
                ]
            except ValidationError as e:
                form.add_error("postcodes", e.message)
                continue

            duplicates = duplicates | (
                seen_values & set(form.cleaned_data["postcodes"])
            )
            seen_values = seen_values | set(form.cleaned_data["postcodes"])

        if duplicates:
            if len(duplicates) > 1:
                message = f"The postcodes {', '.join(duplicates)} appear in multiple responses"
            else:
                message = f"The postcode {', '.join(duplicates)} appears in multiple responses"
            raise ValidationError(message)
