from bc.service_directory.blocks import DirectoryServicesBlock
from bc.utils.blocks import StoryBlock


class LocationPageStoryBlock(StoryBlock):
    directory_services = DirectoryServicesBlock()
