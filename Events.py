from Component import Component
import datetime

class Events(Component):
    def __init__(self, file):
        super().__init__(file)
        self.iscal = True
        self.q = ""
        self.max = 1000
        self.start = '2025-12-14'
        self.end = datetime.datetime.now().strftime('%Y-%m-%d')

    def run(self,pageToken = ""):
        # Call the Gmail API
        start = datetime.datetime.strptime(self.start, '%Y-%m-%d').isoformat() + '-07:00'
        end = datetime.datetime.strptime(self.end, '%Y-%m-%d') + datetime.timedelta(days=1)
        end = end.isoformat() + '-07:00'
        results = self.service.events().list(calendarId='primary',timeMin=start,timeMax=end,singleEvents=True,orderBy='startTime',maxResults=100,q=self.q,pageToken=pageToken).execute()
        if len(self.output) == 0:
            self.output = self.transform(results.get('items', []))
        else:
            self.output.extend(self.transform(results.get('items', [])))
        pageToken = results.get('nextPageToken', '')
        if len(self.output) < self.max and len(pageToken) > 0:
            self.run(pageToken)

    def transform(self,list):
        ret = []
        for x in list:
            y = []
            y.append(x['summary'])
            if 'start' in x.keys() and 'dateTime' in x['start'].keys():
                start = x['start']['dateTime'][0:10]
                if 'end' in x.keys() and 'dateTime' in x['end'].keys():
                    t1 = datetime.datetime.strptime(x['start']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                    t2 = datetime.datetime.strptime(x['end']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                    delta = t2 - t1
                    secs = delta.total_seconds()
                    duration = secs / 3600.0
                else:
                    duration = 0.0
            else:
                start = ''
                duration = 0.0
            y.append(start)
            if 'colorId' in x.keys():
                colorId = int(x['colorId'])
            else:
                colorId = 0
            y.append(colorId)
            # networking = 5 / recruiter = 11 / interview = 10 / negotiation = 9
            if colorId == 5:
                idx = 0
            elif colorId == 11:
                idx = 1
            elif colorId == 10:
                idx = 2
            elif colorId == 9:
                idx = 3
            else:
                idx = -1
            y.append(idx)
            y.append(duration)
            ret.append(y)
        return ret
