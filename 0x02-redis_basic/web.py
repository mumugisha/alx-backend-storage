#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker.
This module caches the HTML content of URLs for a limited time
and tracks how many times each URL has been accessed.
"""

import redis
import requests
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """
    Decorator that tracks how many times a particular URL was accessed
    and caches the result for 10 seconds.

    Args:
        method (function): The function that fetches the HTML content.

    Returns:
        function: A wrapper function that manages caching and counting.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        result_cache_key = "cached:" + url
        count_cache_key = "count:" + url

        result_cache_data = store.get(result_cache_key)

        if result_cache_data:
            return result_cache_data.decode("utf-8")

        store.incr(count_cache_key)

        html = method(url)

        store.set(result_cache_key, html)
        store.expire(result_cache_key, 10)
        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    For testing, return just the status code as a string.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The status code of the HTTP response as a string.
    """
    resp = requests.get(url)
    return str(resp.status_code)


if __name__ == "__main__":
    url = "http://google.com"
    print(get_page(url))
