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

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token2.json'):
        creds = Credentials.from_authorized_user_file(
            r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token2.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Calendar_Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token2.json', 'w') as token:
            token.write(creds.to_json())
    while True:
        operands = ['add', 'view', 'commit', 'search', 'remove', 'get events', 'remove events', 'exit']
        for i, value in enumerate(operands, start=1):
            print(i, value, sep=") ")
        operation = input("Enter an operation: ").lower()
        if operation == 'add':
            des = str(input("Enter description: ")).upper()
            hr = float(input("Enter Hours: "))
            add_event(creds, des, hr)
        if operation == 'view':
            num = int(input("Enter number of days to view: "))
            get_Hours(num)
        if operation == 'commit':
            dated = str(input("Enter date to get hours: "))
            if dated is None or dated == "":
                commit_hours(creds, None)
            else:
                commit_hours(creds, dated)
        if operation == 'search':
            inp = str(input("Enter search date format is YYY-MM-DD: "))
            Search(inp)
        if operation == 'remove':
            inp = str(input("Enter search date format is YYY-MM-DD: "))
            Remove(inp)
        if operation == 'get events':
            inp = input("Enter date: ")
            get_events(creds, inp)
        if operation == 'remove events':
            inp = input("Enter ID: ")
            remove_event(creds, inp)
        if operation == 'exit':
            break
        elif operation not in operands:
            print("Enter a valid operation")


def commit_hours(creds, date):
    service = build('calendar', 'v3', credentials=creds)

    if date is None:
        today = datetime.date.today()
    else:
        try:
            today = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use the format YYYY-MM-DD.")
            return

    start_time = str(today) + "T00:00:00Z"
    end_time = str(today) + "T23:59:59Z"

    events_result = service.events().list(calendarId='primary', timeMin=start_time, timeMax=end_time,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime', timeZone='Europe/London').execute()
    events = events_result.get('items', [])

    if not events:
        print(f'No events found for date {today}.')
        return
    total_duration = datetime.timedelta(seconds=0)

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
    Connection = sqlite3.connect(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Timetable.db')
    cursor = Connection.cursor()
    print("\nOpened database successfully\n")

    formatted_total_duration = total_duration.seconds / 3600
    coding_hours = (today.strftime('%Y-%m-%d'), 'CODING', formatted_total_duration)
    cursor.execute("INSERT INTO hours VALUES(?, ?, ?);", coding_hours)
    Connection.commit()
    print("Coding hours added to database successfully")


def add_event(creds, description: str, duration: float):
    """
    This function adds a desired event to the calendar
    :param description: takes the description of the event to be published
    :param duration: takes in the duration of event

    """
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
    """Gets the days and prints the data from the database
    :param Number_of_days: takes in number of days to fetch the data from the database
    """
    try:
        today = datetime.date.today()
        when_from = today + datetime.timedelta(days=-int(Number_of_days))  # goes back from the day till today
        Connection = sqlite3.connect(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Timetable.db')
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
    """
    Searches for date in the database
    :param date: takes in the date to be searched
    """
    Connection = sqlite3.connect(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Timetable.db')
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
    """
    Deletes the data for the certain date in the database
    :param date: takes in the date to be deleted
    """
    Connection = sqlite3.connect(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Timetable.db')
    Cursor = Connection.cursor()
    Cursor.execute(f"SELECT DATE, HOURS FROM hours WHERE DATE=?", (date,))

    result = Cursor.fetchall()

    if not result:
        print(f"No results found for date: {date}")
    else:
        Cursor.execute("DELETE FROM hours WHERE DATE=?", (date,))
        Connection.commit()
        print(f"Removed entries for date: {date}")


def get_events(creds, date):
    """Takes in date to fetch events from the calendar and provides with the id
    :param date: takes in the date of the events from calendar on that day
    """
    try:
        today = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use the format YYYY-MM-DD.")
        return

    try:
        service = build('calendar', 'v3', credentials=creds)
        start = str(today) + "T00:00:00Z"
        end = str(today) + "T23:59:59Z"
        events_result = service.events().list(calendarId='primary', timeMin=start, timeMax=end,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime', timeZone='Europe/London').execute()
        events = events_result.get('items', [])

        if not events:
            print(f"No events found for date {today}")
        else:
            print("Event IDs on the specified date:")
            for event in events:
                event_id = event['id']
                summary = event.get('summary', 'No summary available')
                print(f"Event ID: {event_id}, Summary: {summary}")
    except HttpError as error:
        print(f"An error occurred: {error}")


def remove_event(creds, event_id):
    """
    Removes event from the google calendar
    :param event_id: takes in a specific id to delete the event
    """
    service = build('calendar', 'v3', credentials=creds)

    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Event with ID {event_id} has been removed from Google Calendar.")
    except HttpError as e:
        if e.resp.status == 404:
            print(f"Event with ID {event_id} was not found in Google Calendar.")
        else:
            print(f"An error occurred while removing the event: {e}")


if __name__ == '__main__':
    main()
