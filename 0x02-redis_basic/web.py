#!/usr/bin/env python3
"""
Implementing a web cache and tracker
"""

import redis
import requests
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """
    Decorator to track how many times a particular URL was accessed
    and cache the result for 10 seconds.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        result_cache_key = f"cached:{url}"
        count_cache_key = f"count:{url}"

    result_cache_data = store.get(result_cache_key)
    if result_cache_data:
        return result_cache_data.decode("utf-8")

        html_content = method(url)

        store.incr(count_cache_key)

        store.setex(result_cache_key, 10, html_content)

        return html_content

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    print(get_page(test_url))
