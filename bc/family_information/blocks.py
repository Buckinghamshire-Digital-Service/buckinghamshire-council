from wagtail import blocks


class TwoCardRowBlock(blocks.StreamBlock):
    card = blocks.PageChooserBlock()

    class Meta:
        label = "Two-card row"
        max_num = 2
        min_num = 2
        template = "patterns/molecules/streamfield/blocks/two_card_row_block.html"


class ThreeCardRowBlock(blocks.StreamBlock):
    card = blocks.PageChooserBlock()

    class Meta:
        label = "Three-card row"
        max_num = 3
        min_num = 3
        template = "patterns/molecules/streamfield/blocks/three_card_row_block.html"
