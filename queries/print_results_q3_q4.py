def print_query3(result):
    print("\n=== QUERY 3 RESULT ===")
    for r in result:
        print({
            "orderkey": r["_id"],
            "revenue": r["revenue"],
            "orderdate": r["orderdate"],
            "shippriority": r["shippriority"]
        })


def print_query4(result):
    print("\n=== QUERY 4 RESULT ===")
    for r in result:
        print({
            "nation": r["_id"],
            "revenue": r["revenue"]
        })
