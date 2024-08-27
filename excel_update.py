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
RANGE_NAME = "Sheet1!A1:Z1000"

def get_credentials():
    credentials_dict = {
        "type": os.environ.get("TYPE"),
        "project_id": os.environ.get("PROJECT_ID"),
        "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
        "private_key": os.environ.get("PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("CLIENT_EMAIL"),
        "client_id": os.environ.get("CLIENT_ID"),
        "auth_uri": os.environ.get("AUTH_URI"),
        "token_uri": os.environ.get("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
        "universe_domain": os.environ.get("UNIVERSE_DOMAIN")
    }
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    return Credentials.from_service_account_info(credentials_dict, scopes=scopes)
    
def fetch_data_to_csv():
    # Authenticate and create the Sheets API service
    creds = get_credentials()
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
        csv_filename = f"latest_excel_data.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print("Conversion complete!\n\n")
    except Exception as e:
        print(f"Error converting to CSV: {e}")
        return None
    
    return df
