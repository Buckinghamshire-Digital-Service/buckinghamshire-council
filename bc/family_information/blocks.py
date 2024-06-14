from wagtail import blocks


class NCardRowBlock(blocks.StreamBlock):
    card = blocks.PageChooserBlock()

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["page_class"] = parent_context["page"]._meta.object_name
        return context


class TwoCardRowBlock(NCardRowBlock):
    class Meta:
        label = "Two-card row"
        max_num = 2
        min_num = 2
        template = "patterns/molecules/streamfield/blocks/two_card_row_block.html"


class ThreeCardRowBlock(NCardRowBlock):
    class Meta:
        label = "Three-card row"
        max_num = 3
        min_num = 3
        template = "patterns/molecules/streamfield/blocks/three_card_row_block.html"
