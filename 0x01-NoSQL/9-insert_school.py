#!/usr/bin/env python3
"""A Python function that inserts a new document in a
collection based on kwargs."""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection.

    Args:
        mongo_collection: The pymongo collection object.
        kwargs: Keyword arguments to represent fields.

    Returns:
        New ID of inserted docs.
    """

    response = mongo_collection.insert_one(kwargs)
    return response.inserted_id
