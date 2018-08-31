# Inside modules
import sys
from time import mktime
from datetime import datetime, timedelta

def print_bar(now_count, max_count):
	max_bar_size = 50
	percent = (now_count*100) // max_count
	bar_num = percent // 2
	if now_count >= max_count:
		bar = "=" * (max_bar_size-1) + ">"
		percent = 100
	elif (bar_num - 1) > 0:
		bar = "=" * (bar_num-1) + ">" + " " * (max_bar_size-bar_num)
	elif bar_num == 1:
		bar = ">" + " " * (max_bar_size-1)
	else:
		bar = " " * max_bar_size
	sys.stdout.write("{}/{} [{}] - {}%\r".format(now_count, max_count, bar, percent))

def waiting(**timeoption):
	start_time = datetime.now()
	start_unixtime = mktime(start_time.timetuple())
	finish_time = start_time + timedelta(**timeoption)
	finish_unixtime = mktime(finish_time.timetuple()) - start_unixtime
	while finish_time > datetime.now():
		print_bar(int(mktime(datetime.now().timetuple()) - start_unixtime), int(finish_unixtime))
	sys.stdout.write("\n")