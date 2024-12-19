import functions
import os
import pandas as pd
from datetime import datetime

# Set maximum column width to prevent truncation
pd.set_option('display.max_colwidth', None)

# File paths for CSVs
base_path = os.path.join(os.path.expanduser("~"), "Desktop", "Python program")
os.makedirs(base_path, exist_ok=True)

user_csv_path = os.path.join(base_path, "user.csv")
credentials_csv_path = os.path.join(base_path, "user_credentials.csv")

def main(user_df):
    user_email = None  # Track if a user is logged in

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Stock Analysis")
        print("4. View User Interaction History")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            email = input("Enter your email: ")
            if not email or "@" not in email or ".com" not in email:
                print("You entered an invalid email.")
                continue
            
            if functions.register_user(email, user_df):
                print("This email is already registered.")
                continue

            password = input("Enter your password: ")
            if password.startswith("0"):
                print('Password cannot start with "0".')
                continue

            confirm_password = input("Confirm your password: ")
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue

            new_user = {'email': email, 'password': password}
            functions.save_to_csv(new_user, user_csv_path)
            user_df = functions.load_csv_as_dataframe(user_csv_path, ['email', 'password'])  # Reload DataFrame
            print("User registered successfully!")

        elif choice == "2": 
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            if functions.authenticate_user(email, password, user_df):
                print("Login successful!")
                user_email = email
            else:
                print("Invalid email or password")

        elif choice == "3":
            if user_email is None:
                print("Please log in to access stock analysis.")
                continue

            stock_ticker = input("Enter the stock ticker (e.g., 1066.KL): ")
            start_date = input("Enter the start date (YYYY-MM-DD, e.g., 2022-01-01): ")
            end_date = input("Enter the end date (YYYY-MM-DD, e.g., 2022-01-31): ")

            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            try:
                data = functions.get_closing_prices(stock_ticker, start_date, end_date)
                if data.empty:
                    print("No data found for the given stock ticker and date range.")
                    continue

                average_closing_price, percentage_change, highest_closing_price, lowest_closing_price = functions.analyze_closing_prices(data)

                print("\nStock Analysis Results:")
                print(f"Average Closing Price: {average_closing_price}")
                print(f"Percentage Change: {percentage_change}%")
                print(f"Highest Closing Price: {highest_closing_price}")
                print(f"Lowest Closing Price: {lowest_closing_price}")

                analysis_results = f"Avg: {average_closing_price}, % Change: {percentage_change}%, High: {highest_closing_price}, Low: {lowest_closing_price}"
                
                new_analysis = {
                    'email': user_email,
                    'stock_ticker': stock_ticker,
                    'analysis_results': analysis_results
                }

                functions.save_to_csv(new_analysis, credentials_csv_path)
                print("Stock analysis results have been saved.")

            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "4":
            print("\nUser Interaction History:")
            credentials_df = functions.read_from_csv(credentials_csv_path)
            print(credentials_df.to_string(index=False))  # Display full DataFrame content

        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from 1 to 5.")

if __name__ == "__main__":
    user_df = functions.load_csv_as_dataframe(user_csv_path, ['email', 'password'])
    main(user_df)
