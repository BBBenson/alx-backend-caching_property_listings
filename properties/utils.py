import logging
from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

# properties/utils.py
CACHE_KEY = "all_properties"
CACHE_TIMEOUT = 3600  # 1 hour (in seconds)

def get_all_properties():
    """
    Retrieves all Property objects, with Redis caching for 1 hour.
    """
    properties = cache.get(CACHE_KEY)

    if properties is None:
        print("Cache miss: Fetching from DB...")
        properties = list(Property.objects.all())  # Convert queryset to list for caching
        cache.set(CACHE_KEY, properties, CACHE_TIMEOUT)
    else:
        print("Cache hit: Loaded from Redis.")

    return properties


logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info()
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    ratio = hits / total if total > 0 else 0
    metrics = {'hits': hits, 'misses': misses, 'hit_ratio': ratio}
    logger.info(f"Cache Metrics: {metrics}")
    return metrics

