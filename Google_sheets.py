import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES= ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1ei6k0qq0_iEjtEiP9T0p2az3dFUZEzTx-RMDezKHxGs"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "Sheets_Credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range="Sheet1!A2:C6").execute()
        for row in range(2,7):
            num1 = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!A{row}").execute().get("values")[0][
                0]

            num2 = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!B{row}").execute().get("values")[0][
                0]
            calculate_res = num1 + num2
            print(f"Processing {num1} and {num2}")

            sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!C{row}",
                                  valueInputOption = "USER_ENTERED", body = {"values": [[f"{calculate_res}"]]}).execute()
            sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!D{row}",
                                  valueInputOption="USER_ENTERED", body={"values": [["DONE"]]}).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()