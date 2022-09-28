from bc.family_information.models import SubsiteHomePage


def is_family_information_site(site):
    return isinstance(site.root_page.specific, SubsiteHomePage)
