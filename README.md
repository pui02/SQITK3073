# SQITK3073
# Stock Selection Tool

## Overview
The **Stock Selection Tool** is a Python application that helps users analyze historical stock closing prices for the Malaysian Market. The program allows user registration, secure login, stock data analysis using the YFinance library, and the ability to save and view user interaction history.

## Features
1. **User Registration and Login**:
   - Register with an email and password.
   - Authenticate existing users.
   - User credentials are stored securely in a CSV file.

2. **Stock Data Retrieval**:
   - Input a stock ticker (e.g., `1066.KL` for Tenaga Nasional Berhad).
   - Fetch historical closing prices for a specified date range using YFinance.

3. **Stock Analysis**:
   - Perform basic analysis on stock closing prices:
     - Average closing price.
     - Percentage change between the first and last closing prices.
     - Highest and lowest closing prices in the specified period.

4. **Data Storage**:
   - Save user interactions, including email, selected stock tickers, and analysis results, in a CSV file.
   - View stored user interaction history.

## Prerequisites
Before running the project, ensure you have the following:
- Python 3.8 or above installed on your system.
- Required Python libraries:
  - `pandas`
  - `yfinance`

Install the required libraries using:
```bash
pip install pandas
pip install yfinance
