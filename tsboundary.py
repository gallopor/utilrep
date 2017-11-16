import time
import datetime
import calendar

'''
 Timestamp of period boundary.
 tsb = NOW SOD EOD SOW EOW SOM EOM
'''
def tsboundary(tsb='NOW', time_ref='TODAY'):
    time_ref = datetime.date.today()
    ds = datetime.time.min
    de = datetime.time.max
    penum = {
        'SOD': datetime.datetime.combine(time_ref, ds),
        'EOD': datetime.datetime.combine(time_ref, de),
        'SOW': datetime.datetime.combine(time_ref - \
                    datetime.timedelta(time_ref.weekday()), ds),     
        'EOW': datetime.datetime.combine(time_ref + \
                    datetime.timedelta(6 - time_ref.weekday()), de),
        'SOM': datetime.datetime.combine(datetime.date(time_ref.year, \
                    time_ref.month, 1), ds),     
        'EOM': datetime.datetime.combine(datetime.date(time_ref.year, \
                    time_ref.month, calendar.monthrange(time_ref.year, \
                    time_ref.month)[1]), de),
    }
    if tsb == 'NOW':
        ts = time.time()
    else:
        ts = time.mktime(penum[tsb].timetuple())
    return ts


if __name__ == "__main__":
    
    for tsb in ['NOW', 'SOD', 'EOD', 'SOW', 'EOW', 'SOM', 'EOM']:
        ts = tsboundary(tsb)
        print(ts)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts)))
    
    
