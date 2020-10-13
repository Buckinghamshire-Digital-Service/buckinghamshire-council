from bc.utils.blocks import BaseStoryBlock, DetailBlock


# Main streamfield block to be inherited by Longform Pages
# Consider if any new blocks are also needed on utils/blocks.py
class LongformStoryBlock(BaseStoryBlock):
    detail = DetailBlock()
