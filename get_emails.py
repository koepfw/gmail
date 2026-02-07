from datetime import date,datetime,timedelta,timezone
import sys
import csv
import pytz

from Days import Days
from Message import Message
from Messages import Messages

# -------------------------
# Helper Functions
# -------------------------
def today_str() -> str:
    today = date.today()
    return today.strftime("%Y-%m-%d")

def move_day(date_str: str, delta: int) -> str:
    """
    Given a date string in YYYY-MM-DD format, return the date moved
    by delta days as a YYYY/MM/DD string.
    """
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    local_date = date + timedelta(days=delta)
    #print(local_date)
    local_tz = pytz.timezone("America/Los_Angeles")
    local_dt = local_tz.localize(datetime(
        local_date.year,
        local_date.month,
        local_date.day,
        0, 0, 0),is_dst=None)
    #print(local_dt)
    utc_dt = local_dt.astimezone(timezone.utc)
    #print(utc_dt)
    utc_epoch = int(utc_dt.timestamp())
    #print(utc_epoch)
    return str(utc_epoch)

now = datetime.now()
today = "./results/results_" + now.strftime("%Y_%m_%d") + ".csv"
file = open(today,"w",newline="",encoding="utf-8")
writer = csv.writer(file)

# run time parameters
if len(sys.argv) >= 2:
    FIRSTDAY = sys.argv[1]
else:
    FIRSTDAY = today_str()
if len(sys.argv) >= 3:
    LASTDAY = sys.argv[2]
else:
    LASTDAY = FIRSTDAY
print(FIRSTDAY + " - " + LASTDAY)

# days since October 1
p = Days(file)
p.start = FIRSTDAY
p.end = LASTDAY
p.execute()
days = {}
for x in p.output:
    days[x] = 0

# 1000 messages
p = Messages(file)
p.q = "in:sent after:" + move_day(FIRSTDAY,0) + " before:" + move_day(LASTDAY,1)
p.max = 5000
p.execute()
messages = p.output
#print(len(messages))

# loop over messages
target_labels = {"Label_36",
                 "Label_45"}
target_subjects = ["catching up and seeking your advice",
                   "[seattlecto] Hiring: OpenAI Seattle",
                   "Werner Koepf - Engineering Leadership",
                   "checking in",
                   "Werner Koepf and Catie Merrick",
                   "thank you",
                   "Werner <> Preply",
                   "connecting",
                   "Werner<>Saf",
                   "resume",
                   "Invitation: Werner - Alan @ Tue Dec 30, 2025 11am - 11:45am (PST) (alan@kipust.com)",
                   "zoom meeting",
                   "Zoom / Meet link"]
for x in messages:
    p = Message(file)
    p.id = x.get('id')
    p.execute()
    day = p.output[0][0]
    labels = p.output[0][3]
    subject = p.output[0][4]
    if day in days.keys():
        if any(label in target_labels for label in labels) or subject in target_subjects:
            days[day] = days[day] + 1
        else:
            print(p.output[0])
            writer.writerow(p.output[0])
    else:
        break

line = ["Day","Emails"]
writer.writerow(line)
for x in days.keys():
    line = str(x) + "," + str(days[x])
    print(line)
    writer.writerow([x,days[x]])

file.close()

print()
print("execution time: ", str(datetime.now()-now))
