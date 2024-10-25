#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """
    Track how many times a particular URL was accessed
    and cache the result for 10 seconds.
    """
    @wraps(method)
    def wrapper(url: str):
        result_cache_key = f"cached:{url}"
        count_cache_key = f"count:{url}"

        # Increment the count first
        store.incr(count_cache_key)

        # Check for cached data
        result_cache_data = store.get(result_cache_key)
        if result_cache_data:
            return result_cache_data.decode("utf-8")

        # If no cached data, fetch from the original URL
        html = method(url)

        # Cache the result and set expiration to 10 seconds
        store.setex(result_cache_key, 10, html)

        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    Return the HTML content instead of just the status code.
    """
    resp = requests.get(url)
    return resp.text  # Return the full HTML content


if __name__ == "__main__":
    url = "http://google.com"
    print(get_page(url))
