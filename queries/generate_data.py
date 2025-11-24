import random
from datetime import datetime, timedelta
from db_connection import get_db

db = get_db()

# -----------------------------------------------------
# CONFIGURACIÓ DE LA QUANTITAT DE DADES
# -----------------------------------------------------
NUM_CUSTOMERS = 50
NUM_SUPPLIERS = 20
NUM_PARTS = 30
NUM_ORDERS = 200
MAX_LINEITEMS_PER_ORDER = 5

# Nacions i regions de TPC-H simplificades
NATIONS = [
    ("SPAIN", "EUROPE"),
    ("FRANCE", "EUROPE"),
    ("GERMANY", "EUROPE"),
    ("USA", "AMERICA"),
    ("CANADA", "AMERICA"),
    ("CHINA", "ASIA"),
    ("JAPAN", "ASIA"),
]

SEGMENTS = ["AUTOMOBILE", "BUILDING", "HOUSEHOLD", "FURNITURE", "MACHINERY"]

# -----------------------------------------------------
# FUNCIÓ PER GENERAR UNA DATA ALEATÒRIA
# -----------------------------------------------------
def random_date(start_year=2018, end_year=2023):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# -----------------------------------------------------
# GENERACIÓ DE CLIENTS
# -----------------------------------------------------
def generate_customers():
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        nation, region = random.choice(NATIONS)
        customers.append({
            "_id": i,
            "name": f"Customer {i}",
            "address": f"Street {i}",
            "phone": f"+34-555-{1000+i}",
            "acctbal": round(random.uniform(1000, 5000), 2),
            "mktsegment": random.choice(SEGMENTS),
            "nation": {
                "nationkey": i % len(NATIONS),
                "name": nation,
                "region": {
                    "regionkey": random.randint(1, 4),
                    "name": region
                }
            }
        })
    db.customers.insert_many(customers)
    print(f"[OK] Inserted {NUM_CUSTOMERS} customers.")

# -----------------------------------------------------
# GENERACIÓ DE SUPPLIERS
# -----------------------------------------------------
def generate_suppliers():
    suppliers = []
    for i in range(1, NUM_SUPPLIERS + 1):
        nation, region = random.choice(NATIONS)
        suppliers.append({
            "_id": 1000 + i,
            "name": f"Supplier {i}",
            "address": f"Supplier Street {i}",
            "phone": f"+34-222-{1000+i}",
            "acctbal": round(random.uniform(3000, 10000), 2),
            "nation": {
                "nationkey": i % len(NATIONS),
                "name": nation,
                "region": {
                    "regionkey": random.randint(1, 4),
                    "name": region
                }
            }
        })
    db.suppliers.insert_many(suppliers)
    print(f"[OK] Inserted {NUM_SUPPLIERS} suppliers.")

# -----------------------------------------------------
# GENERACIÓ DE PARTS
# -----------------------------------------------------
def generate_parts():
    parts = []
    for i in range(1, NUM_PARTS + 1):
        parts.append({
            "_id": 5000 + i,
            "name": f"Part {i}",
            "mfgr": f"MFGR#{random.randint(1,5)}",
            "brand": f"Brand#{random.randint(10,50)}",
            "type": "STANDARD PART",
            "size": random.randint(1, 50),
            "container": "BOX",
            "retailprice": round(random.uniform(10, 500), 2),
            "comment": "Generated part"
        })
    db.parts.insert_many(parts)
    print(f"[OK] Inserted {NUM_PARTS} parts.")

# -----------------------------------------------------
# GENERACIÓ DE ORDERS + LINEITEMS (INCRUSTATS)
# -----------------------------------------------------
def generate_orders():
    orders = []
    for i in range(1, NUM_ORDERS + 1):
        custkey = random.randint(1, NUM_CUSTOMERS)
        orderdate = random_date()
        num_lineitems = random.randint(1, MAX_LINEITEMS_PER_ORDER)

        lineitems = []
        for _ in range(num_lineitems):
            part_id = random.randint(5001, 5000 + NUM_PARTS)
            supp_id = random.randint(1001, 1000 + NUM_SUPPLIERS)

            extended = round(random.uniform(50, 500), 2)
            discount = round(random.uniform(0.00, 0.20), 2)

            shipdate = orderdate + timedelta(days=random.randint(1, 60))

            lineitems.append({
                "partkey": part_id,
                "suppkey": supp_id,
                "quantity": random.randint(1, 20),
                "extendedprice": extended,
                "discount": discount,
                "tax": 0.07,
                "shipdate": shipdate,
                "returnflag": random.choice(["N", "R"]),
                "linestatus": random.choice(["O", "F"])
            })

        orders.append({
            "_id": 70000 + i,
            "custkey": custkey,
            "orderdate": orderdate,
            "shippriority": random.randint(0, 5),
            "clerk": f"Clerk#{random.randint(1,50)}",
            "lineitems": lineitems
        })

    db.orders.insert_many(orders)
    print(f"[OK] Inserted {NUM_ORDERS} orders with embedded lineitems.")

# -----------------------------------------------------
# FUNCIÓ PRINCIPAL
# -----------------------------------------------------
if __name__ == "__main__":
    print("Generating larger dataset...")
    db.customers.drop()
    db.suppliers.drop()
    db.parts.drop()
    db.orders.drop()

    generate_customers()
    generate_suppliers()
    generate_parts()
    generate_orders()

    print("\n[FINISHED] Large dataset generated successfully!")
