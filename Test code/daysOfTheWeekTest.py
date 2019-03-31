import time

WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

day = 0
hour = 0
max_i = 21
i = 0

while max_i > i:
    hour += 8
    if hour >= 24:
        hour = hour - 24
        day += 1

    print('Day: ', day, 'Hour: ', hour, '\t', WEEKDAYS[day % 7], '\n')
    i+=1
