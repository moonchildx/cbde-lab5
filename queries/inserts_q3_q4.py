from datetime import datetime
from db_connection import get_db

db = get_db()

def reset_collections():
    db.customers.drop()
    db.suppliers.drop()
    db.parts.drop()
    db.orders.drop()
    print("[INFO] Collections reset.")

def insert_sample_data():
    # CUSTOMERS
    db.customers.insert_many([
        {
            "_id": 1,
            "name": "Anna Puig",
            "address": "C/ Major 12",
            "phone": "+34-111-222",
            "acctbal": 1500.00,
            "mktsegment": "AUTOMOBILE",
            "nation": {
                "nationkey": 3,
                "name": "SPAIN",
                "region": {
                    "regionkey": 1,
                    "name": "EUROPE"
                }
            }
        }
    ])

    # SUPPLIERS
    db.suppliers.insert_one({
        "_id": 101,
        "name": "Iberia Supply Co.",
        "address": "C/ Indústria 8",
        "phone": "+34-555-666",
        "acctbal": 8000.00,
        "nation": {
            "nationkey": 3,
            "name": "SPAIN",
            "region": {
                "regionkey": 1,
                "name": "EUROPE"
            }
        }
    })

    # PARTS
    db.parts.insert_one({
        "_id": 5001,
        "name": "Part A",
        "mfgr": "MFGR#1",
        "brand": "Brand#23",
        "type": "ECONOMY ANODIZED STEEL",
        "size": 15,
        "container": "SM BOX",
        "retailprice": 120.30,
        "comment": "Example part"
    })

    # ORDERS + LINEITEMS
    db.orders.insert_one({
        "_id": 70001,
        "custkey": 1,
        "orderdate": datetime(2020, 2, 10),
        "shippriority": 0,
        "clerk": "Clerk#0001",
        "lineitems": [
            {
                "partkey": 5001,
                "suppkey": 101,
                "quantity": 3,
                "extendedprice": 120.30 * 3,
                "discount": 0.05,
                "tax": 0.07,
                "shipdate": datetime(2020, 3, 15),
                "returnflag": "N",
                "linestatus": "O"
            }
        ]
    })

    print("[INFO] Sample inserts executed.")


def create_indexes():
    db.customers.create_index({"mktsegment": 1})
    db.orders.create_index({"custkey": 1, "orderdate": 1})
    db.orders.create_index({"lineitems.shipdate": 1})

    db.suppliers.create_index({"nation.region.name": 1})
    db.customers.create_index({"nation.region.name": 1})
    db.orders.create_index({"orderdate": 1})

    print("[INFO] Indexes created.")
