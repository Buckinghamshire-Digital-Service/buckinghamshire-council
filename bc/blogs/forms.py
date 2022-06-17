from wagtail.admin.forms import WagtailAdminPageForm


class BlogPostPageForm(WagtailAdminPageForm):
    def __init__(
        self,
        data=None,
        files=None,
        parent_page=None,
        subscription=None,
        *args,
        **kwargs
    ):
        super().__init__(data, files, parent_page, subscription, *args, **kwargs)
        self.fields["categories"].choices = [
            (category.pk, category.name)
            for category in parent_page.specific.related_categories.all()
        ]
