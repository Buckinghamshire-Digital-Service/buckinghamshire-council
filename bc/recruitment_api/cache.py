import logging

from django.conf import settings
from django.core.cache import caches
from zeep.cache import Base

logger = logging.getLogger(__name__)


class ZeepDjangoBackendCache(Base):
    """A Zeep cache backend that relies on Django's cache configuration"""

    def __init__(self, timeout=3600):
        self._timeout = timeout
        cache_name = getattr(settings, "ZEEP_DJANGO_CACHE_NAME", "default")
        self._cache = caches[cache_name]

    def add(self, url, content):
        logger.debug("Caching contents of %s", url)
        if not isinstance(content, (str, bytes)):
            raise TypeError(
                "a bytes-like object is required, not {}".format(type(content).__name__)
            )
        self._cache.set(url, content, self._timeout)

    def get(self, url):
        value = self._cache.get(url)
        if value is None:
            logger.debug("Cache MISS for %s", url)
        else:
            logger.debug("Cache HIT for %s", url)
        return value
