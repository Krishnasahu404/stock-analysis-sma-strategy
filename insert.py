import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime


DATABASE = "Assignment"
USER = "postgres"
PASSWORD = "krishna"
HOST = "localhost"
PORT = 5432

# Function  read data from Excel
def read_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    df['datetime'] = pd.to_datetime(df['datetime']) 
    return df

#insert data into PostgreSQL
def insert_data(df):
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()

    # Converting DataFrame to list of tuples
    data_tuples = [(
        row['datetime'],
        row['close'],
        row['high'],
        row['low'],
        row['open'],
        row['volume'],
        row['instrument']
    ) for _, row in df.iterrows()]

    insert_query = """
    INSERT INTO ticker_data (date, close, high, low, open, volume, instrument)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (date) DO UPDATE
    SET close = EXCLUDED.close,
        high = EXCLUDED.high,
        low = EXCLUDED.low,
        open = EXCLUDED.open,
        volume = EXCLUDED.volume,
        instrument = EXCLUDED.instrument;
    """
    
    try:
        cur.executemany(insert_query, data_tuples)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


file_path = 'D:/PYTHON_COURSE/assignment/Assingment.xlsx'  #e
data_df = read_excel(file_path)
insert_data(data_df)
