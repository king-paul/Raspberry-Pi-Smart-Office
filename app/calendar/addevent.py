from __future__ import print_function
import datetime
from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
#TODO move area specific code to secure file
tzone = 'Australia/Melbourne'
utc = '10:00'

event = {
  'summary': 'Patient Appointment',
  'location': 'Doctor Office',
  'description': '',
  'start': {
    'dateTime': '2018-10-5T10:00:00+10:00',
    'timeZone': tzone,
  },
  'end': {
    'dateTime': '2018-10-5T10:00:00+10:00',
    'timeZone': tzone,
  },
  'attendees': [
    {'email': 'lpage@example.com'},
  ],
}

def makeAppointment(year,month,day,hour,minute,desc,length):
  endMin = int(minute)+int(length)
  endHour = hour
  if(int(endMin) >= 60):
    endMin=int(endMin)-60
    endHour = int(endHour)+1

  description = "Example Desc"
  startDate = ('%s-%s-%sT%s:%s:00+%s' % (year,month,day,hour,minute,utc))
  endDate = ('%s-%s-%sT%s:%s:00+%s' % (year,month,day,endHour,endMin,utc))

  event['description'] = description
  event['start']['dateTime'] = startDate
  event['end']['dateTime'] = endDate

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    # Make event
    Month = input('Month: ')
    Day = input('Day: ')
    Hour = input('Hour: ')
    Minute= input('Minute: ')
    Length = input('Length(in minutes): ')
    desc= input('desc: ')
    makeAppointment(2018,Month,Day,Hour,Minute,desc,Length)
    # Call the Calendar API
    print("making event:")
    print(event['start'])
    eVent = service.events().insert(calendarId='b5egs9kvn72l4jul5d6n4qomnk@group.calendar.google.com', body=event).execute()
    print('Event created: %s' % (eVent.get('htmlLink')))
	
if __name__ == '__main__':
    main()