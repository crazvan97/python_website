import time
from datetime import datetime, timedelta

my_hour = "0:51"

schedule = datetime.strptime(my_hour, "%H:%M")

print(schedule)