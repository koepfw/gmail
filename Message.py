from datetime import datetime
from Component import Component
import pytz


class Message(Component):
    def __init__(self, file):
        super().__init__(file)
        self.max = 100
        self.id = ""

    def run(self):
        # Call the Gmail API
        results = self.service.users().messages().get(userId='me',id=self.id).execute()
        epoch_ms = int(results.get('internalDate', ''))
        tz = pytz.timezone("America/Los_Angeles")
        dt = datetime.fromtimestamp(epoch_ms / 1000, tz=tz)
        y = []
        y.append(dt.strftime('%Y-%m-%d'))
        y.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
        y.append(results.get('snippet', ''))
        y.append(results.get('labelIds', []))
        headers = results.get('payload', {}).get('headers', [])
        subject = ""
        recipient = ""
        for header in headers:
            if header.get('name') == 'Subject':
                subject = header.get('value')
            if header.get('name') == 'To':
                recipient = header.get('value')
        if subject.startswith("Re: "):
            subject = subject[4:]
        y.append(subject)
        y.append(recipient)
        self.output.append(y)
