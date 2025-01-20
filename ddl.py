from connector import set_connection
import pandas as pd
import duckdb

with open('queries/create_table.sql') as f:
    query=f.read()

with set_connection('duckdb') as duck:
    duck.execute(query)

    supermarket =pd.read_csv("source/supermarket_data_cleaned.csv")
    duck.query("""
        insert into supermarket_data
        select *
        from supermarket;
    """)












