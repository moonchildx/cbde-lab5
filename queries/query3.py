from datetime import datetime
from db_connection import get_db

db = get_db()

def query3(segment, date1, date2):
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "custkey",
                "foreignField": "_id",
                "as": "customer"
            }
        },
        {"$unwind": "$customer"},
        {
            "$match": {
                "customer.mktsegment": segment,
                "orderdate": {"$lt": date1}
            }
        },
        {"$unwind": "$lineitems"},
        {
            "$match": {
                "lineitems.shipdate": {"$gt": date2}
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "revenue": {
                    "$sum": {
                        "$multiply": [
                            "$lineitems.extendedprice",
                            {"$subtract": [1, "$lineitems.discount"]}
                        ]
                    }
                },
                "orderdate": {"$first": "$orderdate"},
                "shippriority": {"$first": "$shippriority"}
            }
        },
        {
            "$sort": {
                "revenue": -1,
                "orderdate": 1
            }
        }
    ]
    return list(db.orders.aggregate(pipeline))
