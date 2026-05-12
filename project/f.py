from datetime import timedelta, datetime

events = [
    {
        "event_decesead_info": "C",
        "event_title": "Event A",
        "event_location": "Brick",
        "date": "2026-02-10",
        "time": datetime(2026, 1, 28, 5, 0),
        "duration": 2
    },
    {
        "event_decesead_info": "C",
        "event_title": "Event B",
        "event_location": "Wall",
        "date": "2026-02-12",
        "time": datetime(2026, 1, 28, 5, 0),
        "duration": 3
    }, 
    {
        "event_decesead_info": "C",
        "event_title": "Event B",
        "event_location": "Wall",
        "date": "2026-02-12",
        "time": datetime(2026, 1, 28, 23, 0),
        "duration": 10
    }
]

updated_events = []
    

for i in events:
    duration =  i['duration']
    start_time = i['time']

    delta = timedelta(
        hours=duration
    )
    end_time = start_time + delta
    print(start_time)
    print(duration)
    print(end_time)

    i['end_time'] = end_time
    updated_events.append(i)
print(updated_events)



# print(events[0]['duration'])
# print(events[1]['duration'])
# print(events[2]['duration']) will be using a library to generate the incriments

# DATE TIME
# duration = 1.5
# delta = timedelta(
#     hours=duration
# )
# start_time = time(5, 0)


# end_time = start_time + delta
# print(delta)
# print("___________________________________")
# print(start_time)
# print("___________________________________")
# print(duration)
# print("___________________________________")
# print(end_time)
# print("___________________________________")