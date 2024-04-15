from django import forms
from django.forms import ValidationError
from django.template.defaultfilters import slugify
from wagtail.admin.forms import WagtailAdminPageForm


class BlogPostPageForm(WagtailAdminPageForm):
    def __init__(
        self,
        data=None,
        files=None,
        parent_page=None,
        subscription=None,
        *args,
        **kwargs,
    ):
        super().__init__(data, files, parent_page, subscription, *args, **kwargs)
        self.fields["categories"].choices = [
            (category.pk, category.name)
            for category in parent_page.specific.blog_categories.all()
        ]


class BlogHomePageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        categories = []

        for form in self.formsets["blog_categories"].forms:

            if form.is_valid():
                cleaned_form_data = form.clean()
                name = cleaned_form_data.get("name")
                slug = slugify(name)
                matches = [category for category in categories if category[0] == slug]
                if matches:
                    for match in matches:
                        form.add_error(
                            "name",
                            ValidationError(
                                (
                                    "This name is too similar to '%(name)s' for use in URLs, "
                                    "as they are both rendered as '%(slug)s'"
                                ),
                                code="invalid",
                                params={"name": match[1], "slug": slug},
                            ),
                        )
                else:
                    categories.append((slug, name))

        return cleaned_data


class BlogAlertSubscriptionForm(forms.Form):
    email = forms.EmailField()
    email.widget.attrs.update(
        {
            "autocomplete": "off",
            "autocapitalize": "off",
            "placeholder": "Enter your email address",
        }
    )


class BlogSubscriptionManageForm(forms.Form):
    subscribe = forms.ChoiceField(
        choices=[
            (True, "Subscribe for all updates"),
            (False, "Unsubscribe"),
        ],
        widget=forms.RadioSelect,
    )
