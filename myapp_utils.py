from datetime import datetime


def unix_time(date_time):

    date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    timestamp = datetime.timestamp(date)
    return timestamp            



def human_time(date_time):
    
    time_list = []
    
    for time in date_time:
        time_list.append(datetime.fromtimestamp(time))

    return time_list




