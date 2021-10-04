import datetime

import factory
import wagtail_factories

from bc.longform import models


class LongformPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.LongformPage

    title = factory.Sequence(lambda n: f"Longform Page {n}")
    last_updated = datetime.date(2021, 1, 1)


class LongformChapterPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.LongformChapterPage

    title = factory.Sequence(lambda n: f"Longform Chapter {n}")
