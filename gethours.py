from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import argparse

# Argument parser to specify task and calendar ID
parser = argparse.ArgumentParser(description="Fetch study hours from Google Calendar.")
parser.add_argument("-t", "--task", required=True, help="Task name to filter calendar events.")
parser.add_argument("-c", "--calendar_id", required=True, help="Calendar ID to fetch events from.")
args = parser.parse_args()

TASK = args.task.lower()
CALENDAR_ID = args.calendar_id
OUTPUT_PATH = "output.txt"

# ACCESS
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # Add your credentials path to your environment variables
SERVICE_ACCOUNT_FILE = credentials_path
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Authenticate and initialize the Calendar API
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Initialize the service
service = build('calendar', 'v3', credentials=credentials)

# Get the start and end of the week (Monday morning to Friday night)
now = datetime.now()
if now.weekday() >= 5:  # Saturday or Sunday
    start_of_week = now + timedelta(days=(7 - now.weekday()))  # Next Monday
else:
    start_of_week = now - timedelta(days=now.weekday())  # Current Monday

# Set start to Monday at 00:00 and end to Friday at 23:59
start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_week = start_of_week + timedelta(days=4, hours=23, minutes=59, seconds=59)

# Convert to ISO format with timezone information for the API
start_of_week_iso = start_of_week.isoformat() + 'Z'
end_of_week_iso = (end_of_week + timedelta(days=1)).isoformat() + 'Z'

def get_study_hours():
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_week_iso,
        timeMax=end_of_week_iso,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    study_hours_per_day = {start_of_week.date() + timedelta(days=i): 0 for i in range(5)}

    for event in events:
        title = event.get('summary', '').lower()
        if title == TASK:
            start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
            duration = (end - start).total_seconds() / 3600
            study_hours_per_day[start.date()] += duration

    return {day.strftime('%A'): hours for day, hours in study_hours_per_day.items()}

if __name__ == '__main__':
    study_hours = get_study_hours()
    total = 0
    with open(OUTPUT_PATH, "w") as file:
        for day, hours in study_hours.items():
            print(f"{day}: {hours:.2f} hours")
            total += hours
    print(f"Total hours: {total:.2f} hours")

