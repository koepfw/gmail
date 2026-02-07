from datetime import datetime
from dateutil import tz
from Component import Component


class Message(Component):
    def __init__(self, file):
        super().__init__(file)
        self.max = 100
        self.id = ""

    def run(self):
        # Call the Gmail API
        results = self.service.users().messages().get(userId='me',id=self.id).execute()
        y = []
        utc = datetime.utcfromtimestamp(int(results.get('internalDate', ''))/1000)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        y.append(local.strftime('%Y-%m-%d'))
        y.append(local.strftime('%Y-%m-%d %H:%M:%S'))
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
