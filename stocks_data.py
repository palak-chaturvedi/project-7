import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# Create a table to store stock data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER
    )
''')
conn.commit()

# Alpha Vantage API Key
api_key = 'JRSQ3SX94LAY4LRK'


# Function to fetch stock data
def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    daily_data = data['Time Series (Daily)']

    for date, info in daily_data.items():
        cursor.execute('''
            INSERT INTO stock_data (date, open, high, low, close, volume)
            VALUES (?,?,?,?,?,?)
        ''', (date, info['1. open'], info['2. high'], info['3. low'], info['4. close'], info['6. volume']))
    conn.commit()


# Fetch stock data for Apple (AAPL)
fetch_stock_data('AAPL')

# Load stock data from the database into a pandas DataFrame
df = pd.read_sql_query("SELECT * from stock_data", conn)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Plot stock data for the past 30 days
recent_data = df.iloc[-30:]
plt.plot(recent_data['date'], recent_data['close'])
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Apple Stock Price (Past 30 Days)')
plt.show()

# Print the current stock price
current_price = df.iloc[-1]['close']
print(f'Current Price: ${current_price}')

# Close the database connection
conn.close()
