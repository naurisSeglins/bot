from datetime import datetime

def do_some_work():
    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time)
    print(unix_time)




