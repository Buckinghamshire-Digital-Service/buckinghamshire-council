from bc.family_information.models import SubsiteHomePage


def is_subsite(site):
    return isinstance(site.root_page.specific, SubsiteHomePage)
