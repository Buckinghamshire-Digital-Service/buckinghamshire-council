import dataclasses
import datetime
import enum
from typing import Any, Dict, NamedTuple, Optional

from django.db.models import TextChoices

import dataclasses_json
from marshmallow import fields as mm_fields


class _DirectoryTuple(NamedTuple):
    api_url: str
    frontend_url: str
    label: str
    api_value: Optional[str] = None


class Directory(enum.Enum):
    FAMILY_INFORMATION_SERVICE = "family-information-service", _DirectoryTuple(
        api_url="https://api.familyinfo.buckinghamshire.gov.uk/api/v1/",
        frontend_url="https://directory.familyinfo.buckinghamshire.gov.uk/",
        label="Family Information Service",
        api_value="bfis",
    )

    def __new__(cls, *args, **kwds) -> "Directory":
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, value: str, directory: _DirectoryTuple) -> None:
        if directory.api_value is None:
            self.api_value = value
        else:
            self.api_value = directory.api_value
        self.label = directory.label
        self.frontend_url = directory.frontend_url
        self.api_url = directory.api_url

    @classmethod
    def get_choices(cls):
        return [(directory.value, directory.label) for directory in cls]


class Collection(TextChoices):
    FAMILY_CENTRES = "family-centres", "Family Centres"


class _CategoryTuple(NamedTuple):
    label: str
    collection: Collection
    api_value: Optional[str] = None
    frontend_value: Optional[str] = None


# These are hard-coded from
# https://manage-directory-listing.buckinghamshire.gov.uk/api/v1/taxonomies


class Category(enum.Enum):
    AMERSHAM_FAMILY_CENTRE = "amersham-family-centre", _CategoryTuple(
        label="Amersham Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )
    BEACONSFIELD_FAMILY_CENTRE = "beaconsfield-family-centre", _CategoryTuple(
        label="Beaconsfield Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )
    BERRYFIELDS_FAMILY_CENTRE_AYLESBURY = (
        "berryfields-family-centre-aylesbury",
        _CategoryTuple(
            label="Berryfields Family Centre, Aylesbury",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    BUCKINGHAM_FAMILY_CENTRE = "buckingham-family-centre", _CategoryTuple(
        label="Buckingham Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )
    BURNHAM_FAMILY_CENTRE = "burnham-family-centre", _CategoryTuple(
        label="Burnham Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )
    CASTLEFIELD_FAMILY_CENTRE_WYCOMBE = (
        "castlefield-family-centre-wycombe",
        _CategoryTuple(
            label="Castlefield Family Centre, Wycombe",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    ELMHURST_FAMILY_CENTRE_AYLESBURY = (
        "elmhurst-family-centre-aylesbury",
        _CategoryTuple(
            label="Elmhurst Family Centre, Aylesbury",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    HAMPDEN_WAY_FAMILY_CENTRE_WYCOMBE = (
        "hampden-way-family-centre-wycombe",
        _CategoryTuple(
            label="Hampden Way Family Centre, Wycombe",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    HITHERCROFT_FAMILY_CENTRE_WYCOMBE = (
        "hithercroft-family-centre-wycombe",
        _CategoryTuple(
            label="Hithercroft Family Centre, Wycombe",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    WING_FAMILY_CENTRE = "wing-family-centre", _CategoryTuple(
        label="Wing Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )
    SOUTHCOURT_FAMILY_CENTRE_PLUS_AYLESBURY = (
        "southcourt-family-centre-plus-aylesbury",
        _CategoryTuple(
            label="Southcourt Family Centre Plus, Aylesbury",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    THE_IVERS_FAMILY_CENTRE = "the-ivers-family-centre", _CategoryTuple(
        label="The Ivers Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )
    NEWTOWN_FAMILY_CENTRE_PLUS_CHESHAM = (
        "newtown-family-centre-plus-chesham",
        _CategoryTuple(
            label="Newtown Family Centre Plus, Chesham",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    MAPLEDEAN_FAMILY_CENTRE_PLUS_WYCOMBE = (
        "mapledean-family-centre-plus-wycombe",
        _CategoryTuple(
            label="Mapledean Family Centre Plus, Wycombe",
            collection=Collection.FAMILY_CENTRES,
        ),
    )
    MARLOW_FAMILY_CENTRE = "marlow-family-centre", _CategoryTuple(
        label="Marlow Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )
    RISBOROUGH_FAMILY_CENTRE = "risborough-family-centre", _CategoryTuple(
        label="Risborough Family Centre",
        collection=Collection.FAMILY_CENTRES,
    )

    def __new__(cls, *args, **kwds) -> "Category":
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, value: str, category: _CategoryTuple) -> None:
        if category.api_value is None:
            self.api_value = value
        else:
            self.api_value = category.api_value

        if category.frontend_value is None:
            self.frontend_value = value
        else:
            self.frontend_value = category.frontend_value

        self.label = category.label
        self.collection = category.collection

    @classmethod
    def get_choices(cls):
        return [(directory.value, directory.label) for directory in cls]


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass
class APIService:
    description: str
    id: int
    name: str
    url: str
    free: Optional[bool]
    local_offer: Optional[Dict[str, Any]]
    updated_at: datetime.datetime = dataclasses.field(
        metadata=dataclasses_json.config(
            encoder=datetime.datetime.isoformat,
            decoder=datetime.datetime.fromisoformat,
            mm_field=mm_fields.DateTime(format="iso"),
        )
    )
