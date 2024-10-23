#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import requests
import redis
from functools import wraps

# Redis connection
store = redis.Redis()


def count_url_access(method):
    """
    Track how many times a particular URL was accessed
    and cache the result for 10 seconds.
    """
    @wraps(method)
    def wrapper(url):
        result_cache_key = "cached:" + url
        count_cache_key = "count:" + url

        result_cache_data = store.get(result_cache_key)
        if result_cache_data:
            return result_cache_data.decode("utf-8")

        html = method(url)

        store.incr(count_cache_key)

        store.setex(result_cache_key, 10, html)

        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    """
    resp = requests.get(url)
    return resp.text
