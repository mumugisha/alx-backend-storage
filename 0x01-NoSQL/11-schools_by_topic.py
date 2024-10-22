#!/usr/bin/env python3
""" 11-main """


def schools_by_topic(mongo_collection, topic):
    """
    """
    school_list = mongo_collection.find({"topics": topic})
    return list(school_list)
