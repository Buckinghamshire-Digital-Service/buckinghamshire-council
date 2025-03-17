from wagtail.blocks import PageChooserBlock


class EmbeddedFormBlock(PageChooserBlock):
    """
    A block that renders a <form> for a given FormPage.
    The user can pick the FormPage using a standard page chooser widget.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, required=True, page_type="forms.FormPage", **kwargs)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        page = context["page"]
        request = context["request"]
        forloop = context.get("forloop", {"counter": None})
        embed_id = value.get_embed_id(suffix=forloop["counter"])

        context["embedding_page"] = page
        context["embedding_id"] = embed_id
        context["page"] = value
        context["form"] = value.get_form(
            page=value,
            user=request.user,
            # If several forms are embedded on the same page we need them
            # to have different ids:
            auto_id=f"id_{embed_id}_%s",
        )

        if request.GET.get("embed_success") == embed_id:
            context["embed_success"] = True

        return context

    class Meta:
        template = "patterns/organisms/form-templates/embedded_form.html"
