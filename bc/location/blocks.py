from bc.service_directory.blocks import DirectoryActivitiesBlock
from bc.utils.blocks import StoryBlock


class LocationPageStoryBlock(StoryBlock):
    directory_activities = DirectoryActivitiesBlock()
