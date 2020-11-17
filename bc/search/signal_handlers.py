from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from bc.search.models import Term
from bc.search.utils import get_synonyms


@receiver([post_save, post_delete], sender=Term)
def cache_synonyms_receiver(**kwargs):
    get_synonyms(force_update=True)
