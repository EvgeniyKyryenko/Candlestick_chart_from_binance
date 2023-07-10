# Binance Data Collection and Flask UI</h1>

This repository contains scripts to collect data from the Binance API 
and display candlestick data and market caps through a Flask UI.

## Prerequisites

 - Python 3.11</li>
 - pip package manager</li>


## Installation

1. Clone the repository:

```bash
   git clone https://github.com/EvgeniyKyryenko/Candlestick_chart_from_binance.git
```

2. Navigate to the project directory:

```bash
   cd binance-data-collection
```

3. Install the required dependencies:

```bash
   pip install -r requirements.txt
```
# Postgres database configuration
1. Go to the directory where `docker-compose.yaml` file is located and run a command
```bash
    docker-compose up -d
```


# Data Collection Script (Task1)

1. Open `collect_data.py` script in text editor
2. Modify the `interval` variable to set the desired interval (e.g., '1d', '4h', '1h').
3. Modify the `symbol` variable to set the desired trading symbol (e.g., 'BTCUSDT', 'ETHUSDT').
4. Run the script:
```bash
    python collect_data.py
```
5. This will collect data from the Binance API for the specified interval and symbol 
and save it in a CSV file with name `{symbol}_{interval}_data.csv`.
7. Use a function `save_data_to_db` and parameters `data` and `table_name` for saving data to database.


# Flask UI (Task 2)

1. Run the Flask application:
```bash
    python app.py
```
2. Open your web browser and go to `http://localhost:5000`.

You should see the Flask UI displaying candlestick data using Plotly 
and a pie chart showing market caps for 10 symbols.

Note: Make sure that you have collected data using 
the data collection script (Task 1) before running the Flask application.

*That's it! You should now be able to run both scripts and access the Flask UI to view the candlestick data and market caps.*