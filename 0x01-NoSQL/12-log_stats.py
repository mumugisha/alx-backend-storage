#!/usr/bin/env python3
"""
Python script that provides some stats
about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stat():
    """
    Connect to MongoDB, retrieve and print the
    number of logs and methods statistics.


    Args:
        None

    Return:
        None
    """
    client = MongoClient()
    mongo_db = client.logs
    collection_db = mongo_db.nginx

    log_count = collection_db.count_documents({})
    print(f"{log_count} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods stats:")

    for method in methods:
        counted_methods = collection_db.count_documents({"method": method})
        print(f"\tmethod {method}: {counted_methods}")

    status_check_counted = collection_db.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check_counted} status check")


if __name__ == "__main__":
    log_stat()
