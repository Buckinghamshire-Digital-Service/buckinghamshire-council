from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from bc.events.models import EventType
from bc.news.models import NewsType
from bc.people.models import PersonType


class EventTypeModelAdmin(ModelAdmin):
    model = EventType
    menu_icon = "tag"


class NewsTypeModelAdmin(ModelAdmin):
    model = NewsType
    menu_icon = "tag"


class PersonTypeModelAdmin(ModelAdmin):
    model = PersonType
    menu_icon = "tag"


class TaxonomiesModelAdminGroup(ModelAdminGroup):
    menu_label = "Taxonomies"
    items = (NewsTypeModelAdmin, EventTypeModelAdmin, PersonTypeModelAdmin)
    menu_icon = "tag"


modeladmin_register(TaxonomiesModelAdminGroup)
