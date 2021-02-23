from django.conf import settings
from django.http import HttpResponse

from utils.caches import get_redis_cache


def get_throttling_cache_key(session_id, url):
    return "{}.{}".format(session_id, url)


def is_url_being_throttled(session_id, url):
    cache = get_redis_cache()
    key = get_throttling_cache_key(session_id, url)
    return bool(cache.get(key))


def get_throttling_timeout(session_id, url):
    cache = get_redis_cache()
    key = get_throttling_cache_key(session_id, url)
    return cache.ttl(key)


def set_throttling_cache(session_id, url, timeout=None):
    cache = get_redis_cache()
    key = get_throttling_cache_key(session_id, url)
    cache.set(key, 1, timeout)


def throttle(timeout=0):

    def deco(f):

        def wrap(*args, **kwargs):
            request = args[0]
            session_id = request.COOKIES[settings.SESSION_COOKIE_NAME]
            url = request.path

            cache_key = get_throttling_cache_key(session_id, url)
            cache = get_redis_cache()

            if is_url_being_throttled(session_id, url):
                ttl = get_throttling_timeout(session_id, url)
                if ttl:
                    return HttpResponse(
                        content='Too many requests: try in {} seconds'.format(ttl),
                        status=429,
                    )

            cache.set(cache_key, 1, timeout)
            response = f(*args, **kwargs)
            if not timeout:
                cache.delete(cache_key)

            return response

        return wrap

    return deco
