from pattern_library.monkey_utils import override_tag

from bc.navigation.templatetags.navigation_tags import register

override_tag(register, name="sidebar")
override_tag(register, name="footerlinks")
