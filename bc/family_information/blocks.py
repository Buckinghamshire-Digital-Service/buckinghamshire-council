from wagtail import blocks


class NCardRowBlock(blocks.StreamBlock):
    card = blocks.PageChooserBlock()

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["page_class"] = parent_context["page"]._meta.object_name
        return context


class CardsBlock(NCardRowBlock):
    """A block that displays 3 pages per row, but accepts more than 3 pages."""

    class Meta:
        label = "Cards"
        min_num = 1
        template = "patterns/molecules/streamfield/blocks/cards_block.html"


class TwoCardRowBlock(NCardRowBlock):
    """A block that only accepts 2 pages, to display the 2 pages in one row."""

    class Meta:
        label = "Two-card row"
        max_num = 2
        min_num = 2
        template = "patterns/molecules/streamfield/blocks/two_card_row_block.html"


class ThreeCardRowBlock(NCardRowBlock):
    """A block that only accepts 3 pages, to display the 3 pages in one row."""

    class Meta:
        label = "Three-card row"
        max_num = 3
        min_num = 3
        template = "patterns/molecules/streamfield/blocks/three_card_row_block.html"
