#!/usr/bin/env python3
"""
Redis basic modules, class, and methods
"""

import redis
from uuid import uuid4
from functools import wraps
from typing import Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    """
    Count how many times methods of Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Store history of inputs and outputs
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """
    Display the history of a particular call
    """
    rep = redis.Redis()
    func_name = fn.__qualname__
    c = rep.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    infis = rep.lrange(f"{func_name}:inputs", 0, -1)
    outfis = rep.lrange(f"{func_name}:outputs", 0, -1)
    for infi, outfi in zip(infis, outfis):
        try:
            infi = infi.decode("utf-8")
        except Exception:
            infi = ""
        try:
            outfi = outfi.decode("utf-8")
        except Exception:
            outfi = ""
        print("{}(*{}) -> {}".format(func_name, infi, outfi))


class Cache:
    """
    A cache class
    """

    def __init__(self):
        """
        Redis private instances
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that takes argument to return a string
        """
        self._key = str(uuid4())
        self._redis.set(self._key, data)
        return self._key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        Convert data to the right format
        """
        mugisha = self._redis.get(key)
        if fn:
            mugisha = fn(mugisha)
        return mugisha

    def get_str(self, key: str) -> str:
        """
        Parameterize cache.get with correct conversion
        """
        mugisha = self._redis.get(key)
        return mugisha.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Parameterize cache.get with correct conversion
        """
        mugisha = self._redis.get(key)
        try:
            mugisha = int(mugisha.decode("utf-8"))
        except Exception:
            mugisha = 0
        return mugisha
