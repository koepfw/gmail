import sys
from datetime import date,datetime,timedelta

from Days import Days
from Events import Events

# -------------------------
# Helper Functions
# -------------------------
def today_str() -> str:
    today = date.today()
    return today.strftime("%Y-%m-%d")

def last_sunday(date_str: str) -> str:
    """
    Given a date string in YYYY-MM-DD format, return the most recent Sunday
    on or before that date, also as a YYYY-MM-DD string.
    """
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    # weekday(): Monday=0 ... Sunday=6
    days_since_sunday = (date.weekday() + 1) % 7
    last_sun = date - timedelta(days=days_since_sunday)
    return last_sun.strftime("%Y-%m-%d")

def day_of_week(date_str: str) -> str:
    """
    Given a date string 'YYYY-MM-DD', return the day of week (e.g. 'Friday').
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    return dt.strftime("%A")

# -------------------------
# Setup
# -------------------------

# run time parameters
if len(sys.argv) >= 2:
    FIRSTDAY = sys.argv[1]
else:
    FIRSTDAY = today_str()
if len(sys.argv) >= 3:
    LASTDAY = sys.argv[2]
else:
    LASTDAY = FIRSTDAY

now = datetime.now()
today = "./results/results_" + now.strftime("%Y_%m_%d") + ".csv"
file = open(today,"w")

# days since July 1
p = Days(file)
p.start = FIRSTDAY
p.end = LASTDAY
p.execute()
days = {}
for x in p.output:
    # networking = 5 / recruiter = 11 / interview = 10 / negotiation = 9
    days[x] = [0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]

# 10 events
p = Events(file)
p.start = FIRSTDAY
p.end = LASTDAY
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

line = "Day,Weekday,Week,Networking #,Recruiter #,Interview #,Negotiation #,Networking H,Recruiter H,Interview H,Negotiation H"
print(line)
file.write("%s\n" % str(line))
for x in days.keys():
    line = str(x) + "," + day_of_week(x) + "," + last_sunday(x) + \
                    "," + str(days[x][0]) + "," + str(days[x][1]) + "," + str(days[x][2]) + "," + str(days[x][3]) + \
                    "," + str(days[x][4]) + "," + str(days[x][5]) + "," + str(days[x][6]) + "," + str(days[x][7])
    print(line)
    file.write("%s\n" % str(line))

file.close()

print()
print("execution time: ", str(datetime.now()-now))
