#!/usr/bin/env python3
"""Python function that updates the list of
topics for schools having a specific name."""

import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Update the topics of the school based on the provided name.

    Args:
        mongo_collection: The pymongo collection object.
        name: Name of the school.
        topics: List of topics in the school.

    Returns:
        None.
    """

    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
