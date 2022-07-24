from datetime import datetime
import time 
import os

from adding_coins_to_db import adding_new_coins_to_db
from calculation import calculate
from new_coins import move_new_coins
from my_wallet import updating_wallet


if __name__ == "__main__":

    dateTimeObj = datetime.now()
    print("first time at: ", dateTimeObj)
    cycle = 9

    time.sleep(6)  # imagine you would like to start work in 6 sec first time
    while True:

        cycleStart = datetime.now()
        print("starting cycle Nr: ",cycle, " at: ", cycleStart)

        if cycle == 10:

            print("checking for new coins at: ", cycleStart)
            adding_new_coins_to_db()


            dateTimeObj = datetime.now()
            print("moving some new coins at: ", dateTimeObj)
            move_new_coins()


            # dateTimeObj = datetime.now()
            # print("buying new coins at: ", dateTimeObj)
            # os.system('node buy_coins.js')


            print("reseting cycle to 0")
            cycle = 0
            cycleStart = datetime.now()


        print("checking wallet how many coins at: ", cycleStart)
        updating_wallet()


        dateTimeObj = datetime.now()
        print("calculating coins at: ", dateTimeObj)
        calculate()


        dateTimeObj = datetime.now()
        print("checking prices in wallet at: ", dateTimeObj)
        os.system('node wallet_coin_price.js')


        dateTimeObj = datetime.now()
        print("checking wallet how many coins at: ", dateTimeObj)
        updating_wallet()


        dateTimeObj = datetime.now()
        print("selling coins at: ", dateTimeObj)
        os.system('node sell_coins.js')


        cycleEnd = datetime.now()
        cycleTime = cycleEnd - cycleStart
        print("cycle time =", cycleTime)


        print("sleeping for 50 seconds at: ", cycleEnd)
        time.sleep(50)  # do work every 50 seconds
        dateTimeObj = datetime.now()
        print("slept for 50 seconds at: ", dateTimeObj)


        # add 1 to the cycle
        cycle +=1


        # space between cycles
        print(" ")
        print(" ")
