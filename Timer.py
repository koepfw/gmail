import datetime

class Timer:
    def __init__(self):
        self.start = datetime.datetime.now()

    def tracksecs(self):
        delta = datetime.datetime.now()-self.start
        ms = str(int(round(delta.microseconds)))
        l = len(ms)
        while l < 6:
            ms = '0' + ms
            l += 1
        return str(delta.seconds) + "." + ms

    def track(self):
        delta = datetime.datetime.now() - self.start
        ms = str(int(round(delta.microseconds)))
        l = len(ms)
        while l < 6:
            ms = '0' + ms
            l += 1
        return str(datetime.timedelta(seconds=delta.seconds)) + "." + ms + " seconds"