from datetime import datetime
from dateutil import tz
from .Component import Component


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
        self.output.append(y)
