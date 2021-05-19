import griddb_python as griddb
import sys
import pandas as pd

factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    nobelprize_data = pd.read_csv("preprocessed.csv") 
    
    for row in nobelprize_data.itertuples(index=False):
        print(f"{row}")

    # View the structure of the data frames
    nobelprize_data.info()

    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )
    
    nobelprize_container = "nobelprize_1901"

    nobelprize_data.info()

    # Create Collection circuits
    nobelprize_containerInfo = griddb.ContainerInfo(nobelprize_container,
                    [["ID", griddb.Type.INTEGER],
        		    ["year", griddb.Type.INTEGER],
         		    ["category", griddb.Type.STRING],
                    ["prize", griddb.Type.STRING],
                    ["prize_share", griddb.Type.STRING],
                    ["laureate_id", griddb.Type.INTEGER],
                    ["laureate_type", griddb.Type.STRING],
                    ["sex", griddb.Type.STRING]],
                    griddb.ContainerType.COLLECTION, True)

    nobelprize_columns = gridstore.put_container(nobelprize_containerInfo)

    print("Container created and columns added")
    
    # Put rows
    # Define the data frames
    nobelprize_columns.put_rows(nobelprize_data)
    
    print("Data Inserted using the DataFrame")

except griddb.GSException as e:
    for i in range(e.get_error_stack_size()):
        print(e.get_message(i))
