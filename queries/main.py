from datetime import datetime
from inserts_q3_q4 import reset_collections, insert_sample_data, create_indexes
from query3 import query3
from query4 import query4
from print_results_q3_q4 import print_query3, print_query4

if __name__ == "__main__":
    reset_collections()
    insert_sample_data()
    create_indexes()

    # Run Query 3
    result3 = query3(
        segment="AUTOMOBILE",
        date1=datetime(2020, 3, 1),
        date2=datetime(2020, 2, 20)
    )
    print_query3(result3)

    # Run Query 4
    result4 = query4(
        region_name="EUROPE",
        date_start=datetime(2020, 1, 1),
        date_end=datetime(2021, 1, 1)
    )
    print_query4(result4)
