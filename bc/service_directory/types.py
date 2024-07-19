from django.db.models import TextChoices

# These are hard-coded from
# https://manage-directory-listing.buckinghamshire.gov.uk/api/v1/taxonomies


class Directory(TextChoices):
    FIS = "bfis", "Family Information Service"


class Taxonomy(TextChoices):
    AMERSHAM_FAMILY_CENTRE = "amersham-family-centre", "Amersham Family Centre"
    BEACONSFIELD_FAMILY_CENTRE = (
        "beaconsfield-family-centre",
        "Beaconsfield Family Centre",
    )
    BERRYFIELDS_FAMILY_CENTRE_AYLESBURY = (
        "berryfields-family-centre_aylesbury",
        "Berryfields Family Centre, Aylesbury",
    )
    BUCKINGHAM_FAMILY_CENTRE = "buckingham-family-centre", "Buckingham Family Centre"
    BURNHAM_FAMILY_CENTRE = "burnham-family-centre", "Burnham Family Centre"
    CASTLEFIELD_FAMILY_CENTRE_WYCOMBE = (
        "castlefield-family-centre_wycombe",
        "Castlefield Family Centre, Wycombe",
    )
    ELMHURST_FAMILY_CENTRE_AYLESBURY = (
        "elmhurst-family-centre_aylesbury",
        "Elmhurst Family Centre, Aylesbury",
    )
    HAMPDEN_WAY_FAMILY_CENTRE_WYCOMBE = (
        "hampden-way-family-centre_wycombe",
        "Hampden Way Family Centre, Wycombe",
    )
    HITHERCROFT_FAMILY_CENTRE_WYCOMBE = (
        "hithercroft-family-centre_wycombe",
        "Hithercroft Family Centre, Wycombe",
    )
    WING_FAMILY_CENTRE = "wing-family-centre", "Wing Family Centre"
    SOUTHCOURT_FAMILY_CENTRE_PLUS_AYLESBURY = (
        "southcourt-family-centre_plus_aylesbury",
        "Southcourt Family Centre Plus, Aylesbury",
    )
    THE_IVERS_FAMILY_CENTRE = "the-ivers-family-centre", "The Ivers Family Centre"
    NEWTOWN_FAMILY_CENTRE_PLUS_CHESHAM = (
        "newtown-family-centre_plus_chesham",
        "Newtown Family Centre Plus, Chesham",
    )
    MAPLEDEAN_FAMILY_CENTRE_PLUS_WYCOMBE = (
        "mapledean-family-centre_plus_wycombe",
        "Mapledean Family Centre Plus, Wycombe",
    )
    MARLOW_FAMILY_CENTRE = "marlow-family-centre", "Marlow Family Centre"
    RISBOROUGH_FAMILY_CENTRE = "risborough-family-centre", "Risborough Family Centre"
