
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import itertools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'CG-DOTW-CAL'

DEVS = ['Edson Lo', 'Luke Misenheimer', 'Chika Hirai', 'Edward Chung', 'Tait Gu', 'Manjunath Amaresh', 'Soumya Mankani']

FIRST_MONDAY = [2018, 4, 9]
LAST_MONDAY = [2018, 6, 4]
DEVS_START_IDX = 2

def createEventObj(devName, startDate, endDate):
    devEmail = devName.replace(' ','.').lower() + '@redfin.com'
    print ('Creating On-Call event for devName: ' + devName + ' devEmail: ' + devEmail + ' startDate: ' + str(startDate) + ' endDate: ' + str(endDate))
    event = {
      'summary': 'On-Call: ' + devName,
      'start': {
        'date': str(startDate),
      },
      'end': {
        'date': str(endDate),
      },
      'attendees': [
        {'email': devEmail},
      ],
    }
    return event


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    currentMonday = datetime.date(FIRST_MONDAY[0], FIRST_MONDAY[1], FIRST_MONDAY[2])
    lastMonday = datetime.date(LAST_MONDAY[0], LAST_MONDAY[1], LAST_MONDAY[2])
    offsetDevs = DEVS[DEVS_START_IDX:] + DEVS[:DEVS_START_IDX]
    devsIter = itertools.cycle(offsetDevs)

    '''
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='redfin.com_fsrm766jm7769tkjrqsdghu2mk@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    '''
    while (currentMonday <= lastMonday):
        event = createEventObj(devsIter.next(), currentMonday, currentMonday + datetime.timedelta(days=5))
        service.events().insert(calendarId='redfin.com_fsrm766jm7769tkjrqsdghu2mk@group.calendar.google.com', body=event).execute()
        currentMonday += datetime.timedelta(days=7)

if __name__ == '__main__':
    main()