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
    if os.path.exists('token2.json'):
        creds = Credentials.from_authorized_user_file('token2.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Calendar_Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token2.json', 'w') as token:
            token.write(creds.to_json())


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
        print('No upcoming events found.')
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
    Connection = sqlite3.connect('Timetable.db')
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


def get_Hours_from_database(Number_of_days: int):
    try:
        today = datetime.date.today()
        when_from = today + datetime.timedelta(days=-int(Number_of_days))  # goes back from the day till today
        Connection = sqlite3.connect('Timetable.db')
        Cursor = Connection.cursor()
        Cursor.execute(f"SELECT DATE, HOURS FROM hours WHERE DATE between ? AND ?", (when_from, today))

        hours = Cursor.fetchall()

        total_hours = 0
        hours_info = []
        for element in hours:
            hours_info.append(f"{element[0]}: {element[1]}")
            total_hours += element[1]
        average_hours = total_hours / float(Number_of_days)
        return hours_info, total_hours, average_hours

    except Exception as e:
        print("An error occurred", e)
        return [], 0, 0


def Search(date):
    """
    Searches for date in the database
    :param date: takes in the date to be searched
    """
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
    """
    Deletes the data for the certain date in the database
    :param date: takes in the date to be deleted
    """
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


def get_events1(creds, date):
    try:
        today = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use the format YYYY-MM-DD.")
        return []

    try:
        service = build('calendar', 'v3', credentials=creds)
        start = str(today) + "T00:00:00Z"
        end = str(today) + "T23:59:59Z"
        events_result = service.events().list(calendarId='primary', timeMin=start, timeMax=end,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime', timeZone='Europe/London').execute()
        events = events_result.get('items', [])

        if not events:
            return []
        else:
            event_list = []
            for event in events:
                event_id = event['id']
                summary = event.get('summary', 'No summary available')
                event_list.append(f"Event ID: {event_id}, Summary: {summary}")
            return event_list
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def remove_event(creds, event_id):
    """
    Removes event from the google calendar
    :param event_id: takes in a specific id to delete the event
    """
    service = build('calendar', 'v3', credentials=creds)

    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Event with ID {event_id} has been removed from Google Calendar.")
        return True
    except HttpError as e:
        if e.resp.status == 404:
            print(f"Event with ID {event_id} was not found in Google Calendar.")
        else:
            print(f"An error occurred while removing the event: {e}")
        return False


if __name__ == '__main__':
    main()
