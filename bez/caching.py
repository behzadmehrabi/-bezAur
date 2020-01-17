import os


import appdirs
from cachelib import FileSystemCache, NullCache


CACHE_DIR = appdirs.user_cache_dir("bez", "behzad")
CACHE_ENTRY_MAX = 256


if os.getenv("BEZ_DISABLE_CACHE"):
    cache = NullCache()
else:
    cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)


def _clear_cache():
    global cache
    if not cache:
        cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)
    return cache.clear()

