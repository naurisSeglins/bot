from datetime import datetime
import time 

from adding_coins_to_db import do_some_work
from moving_new_coins import move_some_coins

if __name__ == "__main__":

    dateTimeObj = datetime.now()
    print("first time at: ", dateTimeObj)

    time.sleep(6)  # imagine you would like to start work in 6 sec first time
    while True:

        dateTimeObj = datetime.now()
        print("doing the work at: ", dateTimeObj)

        do_some_work()

        dateTimeObj = datetime.now()
        print("doing the work at: ", dateTimeObj)

        move_some_coins()

        dateTimeObj = datetime.now()
        print("sleeping for 20 minutes at: ", dateTimeObj)

        time.sleep(1200)  # do work every one hour

        dateTimeObj = datetime.now()
        print("slept for 20 minutes at: ", dateTimeObj)

        