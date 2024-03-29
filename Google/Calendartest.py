import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
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
                'Credentialscalendartest.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        event = {
            "summary": "Pycharm",
            "location": "Somewhere",
            "description": "test use",
            "colorId": 7,
            "start": {
                "dateTime": "2023-07-21T17:00:00",
                "timeZone": "Europe/London"
            },
            "end": {
                "dateTime": "2023-07-21T20:00:00",
                "timeZone": "Europe/London"
            },
            "attendees": [
                {"email": "huzaifasabah@gmail.com"}
            ]
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created {event.get('htmlLink')}")

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
