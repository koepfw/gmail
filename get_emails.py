from datetime import date,datetime,timedelta,timezone
import sys
import csv
import pytz
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from Days import Days
from Message import Message
from Messages import Messages
from Reader import Reader

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
p = Reader(file)
p.input = 'job_index_subjects.csv'
p.execute()
target_subjects = []
for x in p.output:
    target_subjects.append(x[0])

def fetch_message(x):
    p = Message(file)
    p.id = x.get('id')
    p.execute()
    return p.output[0]
# Run all API calls in parallel
with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(fetch_message, x): x for x in messages}
    results = []
    for future in as_completed(futures):
        results.append(future.result())

msg_included = []
msg_excluded = []
for x in results:
    day = x[0]
    labels = x[3]
    subject = x[4]
    if day in days.keys():
        if any(label in target_labels for label in labels) or subject in target_subjects:
            days[day] = days[day] + 1
            msg_included.append(x)
        else:
            msg_excluded.append(x)
    else:
        break

line = ["Included"]
print(line)
writer.writerow(line)
for x in msg_included:
    print(x)
    writer.writerow(x)

line = ["Excluded"]
print(line)
writer.writerow(line)
for x in msg_excluded:
    print(x)
    writer.writerow(x)

line = ["Day","Emails"]
writer.writerow(line)
for x in days.keys():
    line = str(x) + "," + str(days[x])
    print(line)
    writer.writerow([x,days[x]])

file.close()

print()
print("execution time: ", str(datetime.now()-now))
