import csv
from Component import Component


class Reader(Component):
    def __init__(self,file):
        super().__init__(file)
        self.firstline = []

    def run(self):
        with open(self.input, encoding="ISO-8859-1", newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i > 0:
                   self.output.append(row)
                else:
                    self.firstline = row
                i += 1
        self.samples = len(self.output)