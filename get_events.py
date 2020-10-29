import datetime

from gmail.Days import Days
from gmail.Events import Events
from gmail.Message import Message
from gmail.Messages import Messages

now = datetime.datetime.now()
today = "../results/results_" + now.strftime("%Y_%m_%d") + ".txt"
file = open(today,"a+")

# days since July 1
p = Days(file)
p.start = '2020-07-01'
p.execute()
days = {}
for x in p.output:
    # networking = 5 / recruiter = 11 / interview = 10 / negotiation = 9
    days[x] = [0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]

# 10 events
p = Events(file)
p.start = '2020-07-01'
p.end = '2020-10-31'
p.execute()
events = p.output

# loop over events
for x in events:
    start = x[1]
    colorId = x[2]
    idx = x[3]
    duration = x[4]
    if len(start) > 0 and start in days.keys() and idx >= 0:
        days[start][idx] = days[start][idx] + 1
        days[start][idx+4] = days[start][idx+4] + duration

for x in days.keys():
    line = str(x) + "," + str(days[x][0]) + "," + str(days[x][1]) + "," + str(days[x][2]) + "," + str(days[x][3]) + \
                    "," + str(days[x][4]) + "," + str(days[x][5]) + "," + str(days[x][6]) + "," + str(days[x][7])
    print(line)
    file.write("%s\n" % str(line))

file.close()

print()
print("execution time: ", str(datetime.datetime.now()-now))
