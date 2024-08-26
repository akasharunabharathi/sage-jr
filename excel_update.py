import requests
import pandas as pd
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

def fetch_data_to_csv():
    # Authenticate and create the Sheets API service
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=creds)
    # Download the Excel file
    
    # Call the Sheets API to retrieve data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME, ).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return
    
    # Convert to DataFrame
    try:
        df = pd.DataFrame(values[2:], columns=values[1])
        # Convert to CSV
        csv_filename = f"/content/sage-jr/latest_excel_data.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
    except Exception as e:
        print(f"Error converting to CSV: {e}")
        return None
    
    return df
