import pandas as pd

def get_dataset():
    return pd.read_csv("masters_dataset" + ".csv")

def get_query_result():
    master_courses = pd.read_csv("masters_dataset" + ".csv")
    query_result = master_courses.head(10).copy()
    return query_result
