from __future__ import print_function
import config
from google.oauth2 import service_account
from googleapiclient.discovery import build
SAMPLE_SPREADSHEET_ID = '1WEMEY54AgqM0vOMKIr51ctPDYCDUVtw3OFZwJwu3WJE'
service = build('sheets', 'v4', credentials=config.credentials)
# Call the Sheets API


group_list = []
sheet = service.spreadsheets()
result2 = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
res = result2.get('sheets', '')
print(res)
print(len(res))
for i in range(len(res)):
    title = res[i].get("properties", {}).get("title", "Sheet1")
    group_list += [title]
print(group_list)
