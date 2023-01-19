from bc.family_information.models import SubsiteHomePage


def is_subsite(site):
    return isinstance(site.root_page.specific, SubsiteHomePage)


def is_pension_subsite(site):
    return is_subsite(site) and site.root_page.specific.is_pensions_site
