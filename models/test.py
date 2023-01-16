from datetime import datetime
from dateutil.relativedelta import relativedelta

currentTimeDate = datetime.now() + relativedelta(years=2)
currentTime = currentTimeDate.strftime('%Y-%m-%d')

print(currentTime)