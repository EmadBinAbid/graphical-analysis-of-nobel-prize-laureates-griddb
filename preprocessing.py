import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read CSV file
nobelprize_data = pd.read_csv("nobel.csv")

# Drop irrelevant columns
nobelprize_data = nobelprize_data.drop(labels = ["Motivation","Full Name", "Birth Date", 
                                                 "Birth City" , "Birth Country", 
                                                 "Death Date", "Death City" , "Death Country" , 
                                                 "Organization City", "Organization Country", 
                                                 "Organization Name"], axis = 1)

nobelprize_data['Sex'] = nobelprize_data['Sex'].fillna("Not disclosed")


# Add autoincremental ID
nobelprize_data.index.name = 'ID'

# Rename columns
fixColNames = nobelprize_data.rename(columns = {"Year": "year", 
                                                "Category":"category",
                                                "Prize": "prize",
                                                "Prize Share":"prize_share",
                                                "Laureate ID":"laureate_id",
                                                "Laureate Type":"laureate_type",
			                                    "Sex":"sex"})

# Generate a new processed file
fixColNames.to_csv("preprocessed.csv")
