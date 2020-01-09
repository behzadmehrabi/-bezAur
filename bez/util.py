import os

import appdirs
from cachelib import FileSystemCache, NullCache
from termcolor import colored


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

def _cyan(text):
    return  colored(text, "cyan")

def _bcyan(text):
    return colored(text, 'cyan', attrs=['bold'])

def _yellow(text):
    return colored(text, 'yellow')
