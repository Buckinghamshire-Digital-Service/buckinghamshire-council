import factory
import wagtail_factories

from bc.inlineindex import models


class InlineIndexFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.InlineIndex

    title = factory.Sequence(lambda n: f"InlineIndex {n}")
    listing_summary = "Inline Index Summary"


class InlineIndexChildFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.InlineIndexChild

    title = factory.Sequence(lambda n: f"InlineIndexChild {n}")
    listing_summary = "Inline Index Child Summary"
