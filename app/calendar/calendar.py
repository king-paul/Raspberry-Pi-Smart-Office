from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
from datetime import timedelta

# This code was from week 8 lab
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

#def create_calendars():    	
def get_appointments():
    # This code was from week 8 lab
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def add_appointment(name, location, startTime, endTime, doctor, patient):
    date = datetime.now()
    tomorrow = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    time_start = "{}T00:00:00+10:00".format(tomorrow)
    time_end   = "{}T00:00:00+10:00".format(tomorrow)
    event = {     
	'summary': 'Appointment Test',
	'location': 'Lab 1',
	'description': 'Sick Patient; Cold symptoms',
	'start': {
	    'dateTime': time_start,
	    'timeZone': 'Australia/Melbourne',
	},
	'end': {
	    'dateTime': 'time_end',
	    'timeZone': 'Australia/Melbourne',
	},
	'attendees': [
	    {'email': 'patient_x@sick.com'},
	    {'email': 'doc1@treatment.com'},
	],
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
    rm_event = service.events().delete(calendarId='primary', eventId='eventId',
    sendNotification='None').execute()
    print('Event Removed: {}'.format(rm_event.get('htmlLink')))

if __name__ == '__main__':
    get_appointments()
    add_appointment()
   
