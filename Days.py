from datetime import datetime, timedelta
from .Component import Component

class Days(Component):
    def __init__(self, file):
        super().__init__(file)
        self.start = '2020-07-01'
        self.output = []

    def run(self):
        # loop over days
        date = datetime.strptime(self.start, '%Y-%m-%d')
        end_time = datetime.now()
        while date <= end_time:
            self.output.append(date.strftime('%Y-%m-%d'))
            date = date + timedelta(days=1)
