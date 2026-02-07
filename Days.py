from datetime import datetime, timedelta
from Component import Component

class Days(Component):
    def __init__(self, file):
        super().__init__(file)
        self.start = '2025-12-14'
        self.end = datetime.now().strftime('%Y-%m-%d')
        self.output = []

    def run(self):
        # loop over days
        date = datetime.strptime(self.start, '%Y-%m-%d')
        end_time = datetime.strptime(self.end, '%Y-%m-%d')
        while date <= end_time:
            self.output.append(date.strftime('%Y-%m-%d'))
            date = date + timedelta(days=1)
