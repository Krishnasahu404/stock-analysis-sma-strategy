import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

DATABASE = "Assignment"
USER = "postgres"
PASSWORD = "krishna"
HOST = "localhost"
PORT = 5432




def fetch_data():
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    query = "SELECT date, close, high, low, open, volume, instrument FROM ticker_data ORDER BY date"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print("Fetched Data:")
    print(df.head())
    return df


def calculate_sma_strategy(df, short_window=40, long_window=100):
    df['SMA40'] = df['close'].rolling(window=short_window, min_periods=1).mean()
    df['SMA100'] = df['close'].rolling(window=long_window, min_periods=1).mean()
    
    df['Signal'] = 0
    df.loc[short_window:, 'Signal'] = np.where(df['SMA40'][short_window:] > df['SMA100'][short_window:], 1, 0)
    df['Position'] = df['Signal'].diff()
    
    print("SMA Calculation:")
    print(df[['date', 'close', 'SMA40', 'SMA100', 'Signal', 'Position']].head())  # Print the first few rows of the DataFrame with SMAs and signals
    
    return df

# Ploting 
def plot_strategy(df):
    plt.figure(figsize=(12,8))
    plt.plot(df['date'], df['close'], label='Close Price', color='black', alpha=0.5)
    plt.plot(df['date'], df['SMA40'], label='40-Day SMA', color='blue')
    plt.plot(df['date'], df['SMA100'], label='100-Day SMA', color='red')

    plt.plot(df[df['Position'] == 1]['date'], 
             df['SMA40'][df['Position'] == 1], 
             '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(df[df['Position'] == -1]['date'], 
             df['SMA40'][df['Position'] == -1], 
             'v', markersize=10, color='r', lw=0, label='Sell Signal')

    plt.title('SMA Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


df = fetch_data()
df = calculate_sma_strategy(df)
plot_strategy(df)


print("Final DataFrame:")
print(df.tail()) 
