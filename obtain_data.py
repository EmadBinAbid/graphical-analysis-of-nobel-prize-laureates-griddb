
import numpy as np
import griddb_python as griddb
import sys
import pandas as pd
import matplotlib.pyplot as plt

factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    # Get GridStore object
    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    # Define the container names
    nobelprize_container = "nobelprize_1901"

    # Get the containers
    nobelprize_data = gridstore.get_container(nobelprize_container)
    
    # Fetch all rows - circuits_container
    query = nobelprize_data.query("select *")
    rs = query.fetch(False)
    print(f"{nobelprize_container} Data")

    
    # Iterate and create a list
    retrieved_data= []
    while rs.has_next():
        data = rs.next()
        retrieved_data.append(data)
   
    print(retrieved_data)

    # Convert the list to a pandas data frame
    nobelprize_dataframe = pd.DataFrame(retrieved_data, columns=["ID","year","category", "prize", "prize_share","laureate_id","laureate_type", "sex"])

    # Get the data frame details
    print(nobelprize_dataframe)
    nobelprize_dataframe.info()
    
except griddb.GSException as e:
    for i in range(e.get_error_stack_size()):
        print(e.get_message(i))

# Analysis on Gender
gender_wise = nobelprize_dataframe['sex'].value_counts()

genderplot = gender_wise.plot(kind='bar')
genderplot.figure.tight_layout()
genderplot.figure.savefig('gender_wise.png')

# Analysis on Category
category_wise = nobelprize_dataframe['category'].value_counts()

nobelprize_dataframe.groupby(['category','sex']).size().unstack().plot(kind='bar',stacked=True)
plt.tight_layout()
plt.savefig('Category+Gender.png', orientation = 'landscape')
plt.show()

# Time series analysis on Year Group
nobelprize_dataframe["Year_Group"] = pd.cut(nobelprize_dataframe["year"],[1900,1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2016], precision=0, labels=['1900-1910','1910-1920','1920-1930','1930-1940','1940-1950','1950-1960','1960-1970','1970-1980','1980-1990','1990-2000','2000-2010','2010-2016'])    

nobelprize_dataframe.groupby(['Year_Group','category']).size().unstack().plot(kind='bar',stacked=True)
plt.tight_layout()
plt.savefig('Change_over_years.png')
plt.show()
