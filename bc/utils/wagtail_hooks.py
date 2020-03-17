from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from bc.events.models import EventType
from bc.news.models import NewsType
from bc.recruitment.models import JobCategory, JobSubcategory

# from bc.people.models import PersonType


class JobSubcategoryModelAdmin(ModelAdmin):
    model = JobSubcategory
    menu_icon = "tag"
    list_display = ("title", "get_categories_list")


class JobCategoryModelAdmin(ModelAdmin):
    model = JobCategory
    menu_icon = "tag"
    list_display = (
        "title",
        "slug",
        "get_subcategories_list",
        "is_schools_and_early_years",
    )
    search_fields = ("title", "slug")


class EventTypeModelAdmin(ModelAdmin):
    model = EventType
    menu_icon = "tag"


class NewsTypeModelAdmin(ModelAdmin):
    model = NewsType
    menu_icon = "tag"


# class PersonTypeModelAdmin(ModelAdmin):
#     model = PersonType
#     menu_icon = "tag"


class TaxonomiesModelAdminGroup(ModelAdminGroup):
    menu_label = "Taxonomies"
    # items = (NewsTypeModelAdmin, EventTypeModelAdmin, PersonTypeModelAdmin)
    items = (
        NewsTypeModelAdmin,
        EventTypeModelAdmin,
        JobCategoryModelAdmin,
        JobSubcategoryModelAdmin,
    )
    menu_icon = "tag"


modeladmin_register(TaxonomiesModelAdminGroup)
