from google.oauth2 import service_account

token = '2129377067:AAECIAkGnDTJABdUqraDoIz1xL0Vv2mbLrc'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = r'C:\Users\Adminchik\Documents\GitHub\python_bot_edu\service.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
