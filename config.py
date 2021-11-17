from google.oauth2 import service_account
import os
from googleapiclient.discovery import build

token = '2129377067:AAECIAkGnDTJABdUqraDoIz1xL0Vv2mbLrc'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = f'{os.getcwd()}\service.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()
