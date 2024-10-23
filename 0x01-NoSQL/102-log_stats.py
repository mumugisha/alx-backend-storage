#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of
the most present IPs in the collection 'nginx' of the database 'logs'
"""

from pymongo import MongoClient


def nginx_stats_check():
    """
    It provides statistics about Nginx logs in MongoDB
    """

    # Connect to MongoDB and access the 'nginx' collection
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # Print the total number of logs
    number_of_documents = collection.count_documents({})
    print(f"{number_of_documents} logs")

    print("Methods:")
    method_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in method_list:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    print("IPs:")
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    for top_ip in top_ips:
        ip_address = top_ip.get("_id")
        count = top_ip.get("count")
        print(f"\t{ip_address}: {count}")


if __name__ == "__main__":
    nginx_stats_check()
