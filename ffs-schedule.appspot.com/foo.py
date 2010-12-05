# -*- coding: utf-8 -*-

import time
import datetime

n = datetime.datetime.now()
SECS_IN_HOUR = 60 * 60 
curr_ts = time.mktime((n.year, n.month, n.day, n.hour, n.minute, 0, 0, 0, 0))
start_dt = datetime.datetime.fromtimestamp(curr_ts - SECS_IN_HOUR)
print "start=", curr_ts, start_dt
end_dt = datetime.datetime.fromtimestamp(curr_ts + (SECS_IN_HOUR * 23))
print "end=", curr_ts, end_dt
for c in range(-1, 24):
	col_time = datetime.datetime.fromtimestamp(curr_ts + (SECS_IN_HOUR * c))
	print c,  col_time
