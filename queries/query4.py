from db_connection import get_db

db = get_db()

def query4(region_name, date_start, date_end):
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
                "customer.nation.region.name": region_name,
                "orderdate": {"$gte": date_start, "$lt": date_end}
            }
        },
        {"$unwind": "$lineitems"},
        {
            "$lookup": {
                "from": "suppliers",
                "localField": "lineitems.suppkey",
                "foreignField": "_id",
                "as": "supplier"
            }
        },
        {"$unwind": "$supplier"},
        {
            "$match": {
                "$expr": {
                    "$eq": [
                        "$customer.nation.nationkey",
                        "$supplier.nation.nationkey"
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$customer.nation.name",
                "revenue": {
                    "$sum": {
                        "$multiply": [
                            "$lineitems.extendedprice",
                            {"$subtract": [1, "$lineitems.discount"]}
                        ]
                    }
                }
            }
        },
        {"$sort": {"revenue": -1}}
    ]
    return list(db.orders.aggregate(pipeline))
