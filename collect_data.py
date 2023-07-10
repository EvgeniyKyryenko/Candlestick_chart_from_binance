import requests
import pandas as pd
import psycopg2

# get a current price and circulating supply from "coingecko" and calculate a market cap
def get_market_caps(symbols):
    market_caps = {}
    for symbol in symbols:
        url = f'https://api.coingecko.com/api/v3/coins/' + f'{symbol}'
        response = requests.get(url)
        data = response.json()

        coin_price = float(data['market_data']['current_price']['usd'])
        circulating_supply = int(data['market_data']['circulating_supply'])
        market_cap = coin_price * circulating_supply
        market_caps[symbol] = market_cap

    return market_caps

# collect data from a binance api and write this to a dataframe
def collect_data(symbol, interval):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                   'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
        df = pd.DataFrame(data, columns=columns)
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
        return df
    else:
        print("Data collection is failed.")

#  create a new table for data and write it to a new table
def save_data_to_db(data, table_name):
    conn = psycopg2.connect(dbname="binance_db", host="localhost", user="user", password="password", port="8000")
    cur = conn.cursor()
    create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
      open_time TIMESTAMP,
      open NUMERIC,
      high NUMERIC,
      low NUMERIC,
      close NUMERIC,
      volume NUMERIC,
      close_time TIMESTAMP,
      quote_asset_volume NUMERIC,
      number_of_trades INTEGER,
      taker_buy_base_asset_volume NUMERIC,
      taker_buy_quote_asset_volume NUMERIC,
      ignore TEXT
    )"""
    cur.execute(create_table_query)
    conn.commit()

    for _, row in data.iterrows():
        insert_data_query = f"""INSERT INTO {table_name} (open_time,open,high,low,close,volume,close_time,quote_asset_volume,number_of_trades,taker_buy_base_asset_volume,taker_buy_quote_asset_volume,ignore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = tuple(row)
        cur.execute(insert_data_query, values)
    conn.commit()
    cur.close()
    conn.close()

# simple select all from table with "table_name" parameter
def get_all_data_from_db(table_name):
    conn = psycopg2.connect(dbname="binance_db", host="localhost", user="user", password="password", port="8000")
    cur = conn.cursor()
    select_all = f"SELECT * FROM {table_name}"
    cur.execute(select_all)
    data_from_db = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

# drop table functionality
def drop_table(table_name):
    conn = psycopg2.connect(dbname="binance_db", host="localhost", user="user", password="password", port="8000")
    cur = conn.cursor()
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
    cur.execute(drop_table_query)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    # Choose a symbol and interval for collections
    symbol = "ETHUSDT"
    interval = "1h"

    # Collect data from binance
    data = collect_data(symbol, interval)

    # Save data to csv file
    filename = f"{symbol}_{interval}_data.csv"
    data.to_csv(filename, index=False)

    # Save data to database
    # table_name = f"{symbol}_{interval}_data"
    # save_data_to_db(data, table_name)



