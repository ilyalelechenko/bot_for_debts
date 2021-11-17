import config


def find_groups(SAMPLE_SPREADSHEET_ID):
    return config.sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute().get('sheets', '')


def result_columns(SAMPLE_RANGE_NAME, SAMPLE_SPREADSHEET_ID):
    return config.sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                     range=SAMPLE_RANGE_NAME, majorDimension='COLUMNS').execute().get('values', [])


def result_rows(SAMPLE_RANGE_NAME, SAMPLE_SPREADSHEET_ID):
    return config.sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                     range=SAMPLE_RANGE_NAME, majorDimension='ROWS').execute().get('values', [])


