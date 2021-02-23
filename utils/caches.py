from django.core.cache import caches


def get_redis_cache():
    _cache = caches['redis']
    _cache.get(1)  # test connection
    return _cache
