# Misc functions connected with datetime.

import datetime

def time():
    today = datetime.datetime.now()
    hour = '{:02d}'.format(today.hour)
    minute = '{:02d}'.format(today.minute)
    return hour + ':' + minute

def day_of_the_week():
    today = datetime.datetime.now()
    return today.weekday()

def day_and_month():
    today = datetime.datetime.now()
    day = '{:02d}'.format(today.day)
    month = '{:02d}'.format(today.month)
    return day + '/' + month