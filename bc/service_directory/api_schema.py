import dataclasses
import datetime
from typing import Any, Dict, List, Optional

import dataclasses_json
from marshmallow import fields as mm_fields


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass
class Service:
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


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass
class Taxonomy:
    id: int
    label: str
    slug: str
    level: int
    children: List["Taxonomy"] = dataclasses.field(
        metadata=dataclasses_json.config(
            mm_field=mm_fields.List(mm_fields.Nested(lambda: Taxonomy.schema()))
        )
    )
