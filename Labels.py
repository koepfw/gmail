from .Component import Component


class Labels(Component):
    def __init__(self, file):
        super().__init__(file)

    def run(self):
        # Call the Gmail API
        results = self.service.users().labels().list(userId='me').execute()
        self.output = results.get('labels', [])
