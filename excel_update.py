import requests
import pandas as pd
import schedule
import time
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pprint import pprint

from datetime import datetime
from decouple import config

# Load the environment variables
# EXCEL_URL = config("EXCEL_URL")
# SHEET_ID = config("SHEET_ID")
SHEET_ID = "1xgBtPU4p6WX2AJYTdQF3ZpV4Q3Q3ynM4yfXRSC1oCCY"
SERVICE_ACCOUNT_FILE = "/content/sage-jr/token.json"
RANGE_NAME = "Sheet1!A1:Z1000"

def download_and_convert():
    # Authenticate and create the Sheets API service
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=creds)
    # Download the Excel file
    
    # Call the Sheets API to retrieve data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME, ).execute()
    values = result.get('values', [])

    print('Data retrieved from Google Sheet:')
    pprint(values)

    if not values:
        print('No data found.')
        return
    
    # Convert to DataFrame
    try:
        df = pd.DataFrame(values[1:], columns=values[0])
    except Exception as e:
        print(f"Error converting to DataFrame: {e}")
        return

    # Convert to CSV
    csv_filename = f"/content/sage-jr/latest_excel_data.csv"
    print(f"Converting to CSV: {csv_filename}")
    df.to_csv(csv_filename, index=False, encoding='utf-8')

    print(f"Conversion completed. CSV file saved as {csv_filename}")

def job():
    print(f"Starting job at {datetime.now()}")
    try:
        download_and_convert()
    except Exception as e:
        print(f"An error occurred: {e}")
    print(f"Job completed at {datetime.now()}")
    print("Waiting for next run...\n")

# # Schedule the job to run every hour
# schedule.every().hour.do(job)

# # Run the job immediately once
job()

# # Keep the script running
# while True:
#     schedule.run_pending()
#     time.sleep(1)
