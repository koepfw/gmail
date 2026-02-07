from Component import Component


class Messages(Component):
    def __init__(self, file):
        super().__init__(file)
        self.q = ""
        self.max = 1000

    def run(self,pageToken = ""):
        # Call the Gmail API
        results = self.service.users().messages().list(userId='me',includeSpamTrash=False,maxResults=100,q=self.q,pageToken=pageToken).execute()
        if len(self.output) == 0:
            self.output = results.get('messages', [])
        else:
            self.output.extend(results.get('messages', []))
        pageToken = results.get('nextPageToken', '')
        if len(self.output) < self.max and len(pageToken) > 0:
            self.run(pageToken)
