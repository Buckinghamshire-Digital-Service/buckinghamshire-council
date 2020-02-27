from django.db.models import Max

from wagtailorderable.models import Orderable


# TEMPORARY PATCH for wagtailorderable
def patch_orderable():
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.sort_order = (
                self.__class__.objects.aggregate(Max("sort_order"))["sort_order__max"]
                or 0
            ) + 1
        super(Orderable, self).save(*args, **kwargs)

    Orderable.save = save


patch_orderable()
