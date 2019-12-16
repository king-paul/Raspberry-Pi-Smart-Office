from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


# This code was from week 8 lab

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'piot-maps-b24c18239b73.json'
SERVICE_ACCOUNT_NAME = 'piot-maps@appspot.gserviceaccount.com'
CAL_ID = 't8tlnde0s22pfr86am7hjgp69g@group.calendar.google.com'

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

#def create_calendars():

def get_appointments():
    # This code was from week 8 lab
    """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
    """
# Call the Calendar API
now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='CAL_ID', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
events = events_result.get('items', [])
if not events:
                                              print('No upcoming events found.')
for event in events:
                                              start = event['start'].get('dateTime', event['start'].get('date'))
                                              print(start, event['summary'])

def add_appointment(options):
    date = datetime.now()
    tomorrow = (date + timedelta(days=1)).strftime("%d-%m-%Y")
    time_start = "{}T06:00:00+10:00".format(tomorrow)
    time_end   = "{}T07:00:00+10:00".format(tomorrow)


event = {
    
        'summary': options.summmary,
        'location': options.location ,
        'start': {
            'dateTime': options.date, """ date from form, add time"""
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'dateTime': '2018-10-04T10:00:00', """15mins after appointment start"""
            'timeZone': 'Australia/Melbourne',
        },
        'attendees': options.attendees, """ email address"""
            
        'reminders': {
            'useDefault': False,
            'overrides': [
                          {'method': 'email', 'minutes': 5},
                          {'method': 'popup', 'minutes': 10},
                        ],
                     }
    }

event = service.events().insert(calendarId='primary', body=event).execute()
print('Event created: {}'.format(event.get('htmlLink')))


def cancel_appointment():
    rm_event = service.events().delete(calendarId='CAL_ID', eventId='eventId',
                                       sendNotification='None').execute()
    print('Event Removed: {}'.format(rm_event.get('htmlLink')))

if __name__ == '__main__':
    get_appointments()
    add_appointment()

