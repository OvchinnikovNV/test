from datetime import timedelta
from operator import itemgetter


begin = timedelta(hours=9)
end = timedelta(hours=21)
gap = timedelta(minutes=30)
busy = [ {'start' : '10:30', 'stop' : '10:50' }, {'start' : '18:40', 'stop' : '18:50'},
        {'start' : '14:40', 'stop' : '15:50'}, {'start' : '16:40', 'stop' : '17:20' }, {'start' : '20:05', 'stop' : '20:20' }]
        
busy = sorted(busy, key=itemgetter('start') )
gaps = []

for i in range(len(busy) + 1):
    if i == len(busy):
        tmp = end
    else:
        b = busy[i]
        tmp = b['start'].split(':')
        tmp = timedelta(hours=int(tmp[0]), minutes=int(tmp[1]))
    
    for i in range((tmp - begin) // gap):
        gaps.append({'start': str(begin)[:-3], 'stop': str(begin + gap)[:-3]})
        begin += gap
    
    if i < len(busy):
        tmp = b['stop'].split(':')
        begin = timedelta(hours=int(tmp[0]), minutes=int(tmp[1]))
        
for i in gaps:
    print(i)

'''
Output:
{'start': '9:00', 'stop': '9:30'}
{'start': '9:30', 'stop': '10:00'}
{'start': '10:00', 'stop': '10:30'}
{'start': '10:50', 'stop': '11:20'}
{'start': '11:20', 'stop': '11:50'}
{'start': '11:50', 'stop': '12:20'}
{'start': '12:20', 'stop': '12:50'}
{'start': '12:50', 'stop': '13:20'}
{'start': '13:20', 'stop': '13:50'}
{'start': '13:50', 'stop': '14:20'}
{'start': '14:20', 'stop': '14:50'}
{'start': '14:50', 'stop': '15:20'}
{'start': '15:20', 'stop': '15:50'}
{'start': '15:50', 'stop': '16:20'}
{'start': '17:20', 'stop': '17:50'}
{'start': '17:50', 'stop': '18:20'}
{'start': '18:50', 'stop': '19:20'}
{'start': '19:20', 'stop': '19:50'}
{'start': '20:20', 'stop': '20:50'}
'''
