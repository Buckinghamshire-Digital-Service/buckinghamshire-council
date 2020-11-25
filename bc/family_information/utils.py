from bc.family_information.models import FamilyInformationHomePage


def is_family_information_site(site):
    return isinstance(site.root_page.specific, FamilyInformationHomePage)
