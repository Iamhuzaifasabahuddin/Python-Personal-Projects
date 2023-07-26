import datetime
import os.path
import sqlite3
from sys import argv

from dateutil import parser  # type: ignore

from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

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
    while True:
        operation = input("Enter an operation add, commit, view, search, remove, or exit: ").lower()
        if operation == 'add':
            des = str(input("Enter description: ")).upper()
            hr = float(input("Enter Hours: "))
            add_event(creds, des, hr)
        if operation == 'view':
            num = int(input("Enter number of days to view: "))
            get_Hours(num)
        if operation == 'commit':
            commit_hours(creds)
        if operation == 'search':
            inp = str(input("Enter search date format is YYY-MM-DD: "))
            Search(inp)
        if operation == 'remove':
            inp = str(input("Enter search date format is YYY-MM-DD: "))
            Remove(inp)
        if operation == 'exit':
            break
        elif operation not in ['add', 'view', 'commit', 'search', 'remove', 'exit']:
            print("Enter a valid operation")


def commit_hours(creds):
    service = build('calendar', 'v3', credentials=creds)

    today = datetime.date.today()
    start_time = str(today) + "T00:00:00Z"
    end_time = str(today) + "T23:59:59Z"

    events_result = service.events().list(calendarId='primary', timeMin=start_time, timeMax=end_time,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime', timeZone='Europe/London').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return
    total_duration = datetime.timedelta(
        seconds=0,
        minutes=0,
        hours=0,
    )

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        start_formatted = parser.isoparse(start)  # changing the start time to datetime format
        end_formatted = parser.isoparse(end)  # changing the end time to datetime format
        duration = end_formatted - start_formatted

        total_duration += duration
        print(f"{event['summary'].capitalize()}, duration: {duration}")
    print(f"Total duration: {total_duration} Hours")

    # adding the hours to the database
    Connection = sqlite3.connect('Timetable.db')
    cursor = Connection.cursor()
    print("\nOpened database successfully\n")
    date = datetime.date.today()

    formatted_total_duration = total_duration.seconds / 60 / 60
    coding_hours = (date, 'CODING', formatted_total_duration)
    cursor.execute("INSERT INTO hours VALUES(?, ?, ?);", coding_hours)
    Connection.commit()
    print("Coding hours added to database successfully")


def add_event(creds, description: str, duration: float):
    try:
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow() + datetime.timedelta(hours=float(duration))
        start_time_formatted = start_time.isoformat() + 'Z'
        end_time_formatted = end_time.isoformat() + 'Z'

        event = {
            'summary': description,
            'description': 'This is an event created every time I open PyCharm.',
            'colorId': 7,
            'start': {
                'dateTime': start_time_formatted,
                'timeZone': 'Europe/London',  # Replace with your time zone, e.g., 'America/New_York'
            },
            'end': {
                'dateTime': end_time_formatted,
                'timeZone': 'Europe/London',
            },
        }

        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
    except HttpError as error:
        print('An error occurred: %s' % error)


def get_Hours(Number_of_days: int):
    try:
        today = datetime.date.today()
        when_from = today + datetime.timedelta(days=-int(Number_of_days)) # goes back from the day till today
        Connection = sqlite3.connect('Timetable.db')
        Cursor = Connection.cursor()
        Cursor.execute(f"SELECT DATE, HOURS FROM hours WHERE DATE between ? AND ?", (when_from, today))

        hours = Cursor.fetchall()

        total_hours = 0
        for element in hours:
            print(f"{element[0]}: {element[1]}")
            total_hours += element[1]
        print(f"\nTotal hours: {total_hours}")
        print(f"Average hours: {total_hours / float(Number_of_days):.2f}")

    except Exception as e:
        print("An error occurred", e)


def Search(date):
    Connection = sqlite3.connect('Timetable.db')
    Cursor = Connection.cursor()
    Cursor.execute(f"SELECT DATE, HOURS FROM hours WHERE DATE=?", (date,))

    result = Cursor.fetchall()

    if not result:
        print(f"No results found for date: {date}")
    else:
        print("Getting results...")
        for row in result:
            print(f"Date: {row[0]}, Hours: {row[1]}")


def Remove(date):
    Connection = sqlite3.connect('Timetable.db')
    Cursor = Connection.cursor()
    Cursor.execute(f"SELECT DATE, HOURS FROM hours WHERE DATE=?", (date,))

    result = Cursor.fetchall()

    if not result:
        print(f"No results found for date: {date}")
    else:
        Cursor.execute("DELETE FROM hours WHERE DATE=?", (date,))
        Connection.commit()
        print(f"Removed entries for date: {date}")


if __name__ == '__main__':
    main()
