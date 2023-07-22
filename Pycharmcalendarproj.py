import datetime
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token2.json'):
        creds = Credentials.from_authorized_user_file('token2.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Credentialsmain.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token2.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        work_duration = datetime.timedelta(hours=1)  # Set the duration you want to work (e.g., 2 hours)

        start_time = datetime.datetime.utcnow()
        end_time = start_time + work_duration

        event = {
            'summary': 'PyCharm Event',
            'description': 'This is an event created every time I open PyCharm.',
            'colorId': 7,
            'start': {
                'dateTime': start_time.isoformat() + 'Z',
                'timeZone': 'Europe/London',  # Replace with your time zone, e.g., 'America/New_York'
            },
            'end': {
                'dateTime': end_time.isoformat() + 'Z',
                'timeZone': 'Europe/London',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
