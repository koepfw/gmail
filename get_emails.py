import datetime

from gmail.Days import Days
from gmail.Message import Message
from gmail.Messages import Messages

now = datetime.datetime.now()
today = "../results/results_" + now.strftime("%Y_%m_%d") + ".txt"
file = open(today,"a+")

# days since October 1
p = Days(file)
p.start = '2020-10-15'
p.execute()
days = {}
for x in p.output:
    days[x] = 0

# 1000 messages
p = Messages(file)
p.q = "in:sent"
p.max = 5000
p.execute()
messages = p.output

# loop over messages
for x in messages:
    p = Message(file)
    p.id = x.get('id')
    p.execute()
    print(p.output[0])
    day = p.output[0][0]
    if day in days.keys():
        days[day] = days[day] + 1
    else:
        break

for x in days.keys():
    line = str(x) + "," + str(days[x])
    print(line)
    file.write("%s\n" % str(line))

file.close()

print()
print("execution time: ", str(datetime.datetime.now()-now))
