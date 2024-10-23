#!/usr/bin/env python3
"""A script that lists all documents with name
starting by Holberton in the collection school
"""


def top_students(mongo_collection):
    """
    Return all students sorted by their average score.
    """
    top_student = mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_student
