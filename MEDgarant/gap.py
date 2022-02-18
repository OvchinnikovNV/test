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

    for j in range((tmp - begin) // gap):
        gaps.append({'start': str(begin)[:-3], 'stop': str(begin + gap)[:-3]})
        begin += gap
    
    if i < len(busy):
        tmp = b['stop'].split(':')
        begin = timedelta(hours=int(tmp[0]), minutes=int(tmp[1]))
        
for i in gaps:
    print(i)

