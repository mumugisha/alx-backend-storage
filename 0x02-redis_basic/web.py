#!/usr/bin/env python3
"""Redis web server"""

import requests
import redis
import time

r = redis.Redis(host="localhost", port=6379, db=0)


def get_page(url: str) -> str:
    """Get page from url and keeps a count record of visiting times"""
    cache_key = f"page:{url}"
    count_key = f"count:{url}"

    cached_page = r.get(cache_key)

    if cached_page:
        print("Returning cached page...")
        return cached_page.decode("utf-8")

    print("Fetching new page...")
    response = requests.get(url)

    r.setex(cache_key, 10, response.text)

    r.incr(count_key)

    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"

    print(get_page(url))

    time.sleep(2)

    print(get_page(url))

    time.sleep(11)

    print(get_page(url))
