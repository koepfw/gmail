from __future__ import print_function
import pickle
import random
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Timer import Timer

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/gmail.readonly',]

class Component():
    def __init__(self,file):
        self.timer = Timer()
        self.file = file
        self.service = None
        self.output = []
        self.idx = -1
        self.verbose = False
        self.iscal = False

    def execute(self):
        self.write("\n*** " + type(self).__name__)
        self.prep()
        self.run()
        self.print()
        self.finish()

    def prep(self):
        """Shows basic usage of the Gmail API.
            Lists the user's Gmail labels.
            """
        creds = None
        if not self.iscal:
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            self.service = build('gmail', 'v1', credentials=creds)
        else:
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token_cal.pickle'):
                with open('token_cal.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token_cal.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            self.service = build('calendar', 'v3', credentials=creds)

    def print(self):
        l = len(self.output)
        self.write(str(l) + ' rows')
        if l > 0:
            if self.idx < 0:
                self.idx = random.randint(0, l-1)
            if type(self.output[self.idx]).__name__ == 'list':
                line = 'row ' + str(self.idx) + ': ' + ' - '.join(str(v) for v in self.output[self.idx])
            else:
                line = 'row ' + str(self.idx) + ': ' + str(self.output[self.idx])
            self.write(line)

    def finish(self):
        self.write("*** " + type(self).__name__ + " - " + self.timer.tracksecs())


    def write(self,line):
        if self.verbose:
            print(line)
            try:
                self.file.write("%s\n" % str(line))
            except:
                self.file.write("%s\n" % str(line).encode("utf-8"))


