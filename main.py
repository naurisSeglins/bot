from datetime import datetime
import time 
import os

from adding_coins_to_db import do_some_work
from moving_new_coins import move_some_coins
from my_wallet import checking_wallet


if __name__ == "__main__":

    dateTimeObj = datetime.now()
    print("first time at: ", dateTimeObj)
    cycle = 1

    time.sleep(6)  # imagine you would like to start work in 6 sec first time
    while True:
        cycleStart = datetime.now()

        print("Cycle nr.",cycle)

        if cycle == 10:

            print("doing the work at: ", cycleStart)

            do_some_work()

            dateTimeObj = datetime.now()
            print("moving some new coins at: ", dateTimeObj)

            move_some_coins()
            print("reseting cycle")
            cycle = 0
        
        print("moving new coins to wallet at: ", cycleStart)

        checking_wallet()

        dateTimeObj = datetime.now()
        print("checking prices in wallet at: ", dateTimeObj)

        os.system('node wallet_coin_price.js')

        # dateTimeObj = datetime.now()
        # print("buying new coins at: ", dateTimeObj)

        # os.system('node buy_coins.js')
        # os.system('node sell_coins_git_yt.js')

        cycleEnd = datetime.now()

        cycleTime = cycleEnd - cycleStart
        print("cycle time =", cycleTime)

        print("sleeping for 50 seconds at: ", cycleEnd)

        time.sleep(50)  # do work every one hour

        cycle +=1

        dateTimeObj = datetime.now()
        print("slept for 50 seconds at: ", dateTimeObj)
        # space between cycles
        print(" ")
        print(" ")


        