#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from functools import wraps

# Redis connection
store = redis.Redis()


def track_url_access(method):
    """
    Track how many times a particular URL was accessed
    and cache the result for 10 seconds.
    """
    @wraps(method)
    def wrapper(url: str):
        # Cache keys for storing the result and count
        result_cache_key = "cached:" + url
        count_cache_key = "count:" + url

        result_cache_data = store.get(result_cache_key)

        if result_cache_data:
            # Return cached data if found
            return result_cache_data.decode("utf-8")

        store.incr(count_cache_key)

        html = method(url)

        store.set(result_cache_key, html)
        store.expire(result_cache_key, 10)

        return html

    return wrapper


@track_url_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    """
    resp = requests.get(url)
    return resp.text


if __name__ == "__main__":
    url = "http://google.com"
    print(get_page(url))
