import datetime
import math
import re

from django.utils.html import strip_tags

def count_words(html_string):
	word_strings=strip_tags(html_string)
	matching_words=re.findall(r'\w+',word_strings)
	count=len(matching_words)
	return count
def get_read_time(html_string):
	count=count_words(html_string)
	read_time_min=math.ceil(count/200.0)
	# read_time_sec=read_time_min*60
	# read_time=str(datetime.timedelta(seconds=read_time_sec))
	read_time=str(datetime.timedelta(minutes=read_time_min)) #str is ready for fiels
	return read_time