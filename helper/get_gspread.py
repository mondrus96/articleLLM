import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def get_gspread(gspread_locs):
    # Set up the API scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Authenticate using the JSON key file
    creds = ServiceAccountCredentials.from_json_keyfile_name(gspread_locs["config_loc"], scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet by its URL
    spreadsheet = client.open_by_url(gspread_locs["sheet_url"])

    # Select the first sheet and print its data
    worksheet = spreadsheet.worksheet(gspread_locs["sheet_name"])
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df