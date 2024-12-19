import yfinance as yf
import pandas as pd
import os
import csv

def load_csv_as_dataframe(filename, fieldnames):
    """Load a CSV file as a Pandas DataFrame, create it if it doesn't exist."""
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=fieldnames)
        df.to_csv(filename, index=False)
        return df

def register_user(email, df):
    """Check if an email is already registered."""
    return email in df['email'].values

def authenticate_user(email, password, df):
    """Verify user login credentials."""
    user = df[(df['email'] == email) & (df['password'] == password)]
    return not user.empty

def get_closing_prices(ticker, start_date, end_date):
    """Fetch historical closing prices using YFinance."""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print("No data found for the specified stock ticker and date range.")
            return pd.DataFrame()
        return data
    except Exception as e:
        print(f"An error occurred while fetching stock data: {e}")
        return pd.DataFrame()

def analyze_closing_prices(data):
    """Perform basic analysis on the closing prices."""
    if data is None or 'Close' not in data:
        print("No closing price data available for analysis.")
        return None, None, None, None

    try:
        average_closing_price = data['Close'].mean().item()
        percentage_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100).item()
        highest_closing_price = data['Close'].max().item()
        lowest_closing_price = data['Close'].min().item()

        return average_closing_price, percentage_change, highest_closing_price, lowest_closing_price
    except Exception as e:
        print(f"An error occurred while analyzing stock data: {e}")
        return None, None, None, None

def save_to_csv(data, filename):
    """Save user interactions to a CSV file."""
    file_exists = os.path.exists(filename)
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow({key: str(value) for key, value in data.items()})

def read_from_csv(filename):
    """Retrieve and display saved data from the CSV file."""
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        return data
    else:
        print("No data found.")
        return pd.DataFrame()
