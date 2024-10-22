#!/usr/bin/env python3
"""A Python function that lists all documents in a collection."""

import pymongo


def list_all(mongo_collection):
    """
    Function that lists all documents in a collection.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of documents in the collection or an empty
        list if no documents are found.
    """

    if mongo_collection is None:
        return []

    return list(mongo_collection.find()) or []
