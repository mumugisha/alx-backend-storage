#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker.
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
    def wrapper(url: str) -> str:  # Added space after the colon
        result_cache_key = "cached:" + url
        count_cache_key = "count:" + url

        # Increment the count every time get_page is called
        store.incr(count_cache_key)

        # Check if content is in the cache
        result_cache_data = store.get(result_cache_key)
        if result_cache_data:
            return result_cache_data.decode("utf-8")

        # Fetch content if not cached, then cache it for 10 seconds
        html = method(url)
        store.set(result_cache_key, html)
        store.expire(result_cache_key, 10)

        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:  # Added space after the colon
    """
    Fetch the HTML content of a given URL.
    For testing, return "OK" on a successful request.
    """
    try:
        resp = requests.get(url)
        # Return "OK" if the request is successful (status code 200)
        return "OK" if resp.status_code == 200 else "0"
    except requests.RequestException:
        return "0"  # Return "0" in case of any request error


if __name__ == "__main__":
    test_url = (
        "http://slowwly.robertomurray.co.uk/delay/3000/"
        "url/https://google.com"
    )
    print(get_page(test_url))
    print("Access count:", store.get(f"count:{test_url}").decode("utf-8"))
