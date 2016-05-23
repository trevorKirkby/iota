from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import iso8601


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
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


def get_calendar_id(service, name):
    """
    Use the Google calendar API to find the id string associated with the
    specified calendar name. Raises a RuntimeError if the calendar is not found.
    """
    calendar_id = None
    results = service.calendarList().list().execute()
    for cal in results.get('items', []):
        if cal['summary'] == name:
            return cal['id']
    raise RuntimeError('No such calendar named "{}".'.format(name))


def get_future_events(service, calendar_id, days):
    """
    Use the Google calendar API to retrieve future events from the specified
    calendar over the specified number of days.
    """
    if days <= 0 or days > 10:
        raise ValueError('Value of days must be in the range 1-10.')
    print('Getting future events for the next {} days.'.format(days))
    now = datetime.datetime.utcnow()
    timeMin = now.isoformat() + 'Z' # 'Z' indicates UTC time
    timeMax = (now + datetime.timedelta(days=days)).isoformat() + 'Z'
    results = service.events().list(
        calendarId=calendar_id, timeMin=timeMin, timeMax=timeMax, singleEvents=True,
        orderBy='startTime').execute()
    return results.get('items', [])


def main():
    # Initialize the Google calendar API.
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Lookup the calendar we will use for scheduling.
    calendar_id = get_calendar_id(service, 'iota')
    print('Using calendar id:', calendar_id)

    events = get_future_events(service, calendar_id, days=3)
    isofmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    for e in events:
        start = iso8601.parse_date(e['start'].get('dateTime'))
        stop = iso8601.parse_date(e['end'].get('dateTime'))
        # How to check for all-day event?
        print('{} ON AT {} FOR {}'.format(e['summary'], start.ctime(), stop - start))


if __name__ == '__main__':
    main()
