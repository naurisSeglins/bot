from datetime import datetime
import time 
import os

from adding_coins_to_db import adding_new_coins_to_db
from calculation import calculate_wallet
from calculation import calculate_new_coins
from new_coins import move_new_coins
from my_wallet import updating_wallet
from sell_coins import decimal_fixing


if __name__ == "__main__":

    dateTimeObj = datetime.now()
    print("first time at: ", dateTimeObj)
    cycle = 1

    time.sleep(6)  # imagine you would like to start work in 6 sec first time
    while True:

        cycleStart = datetime.now()
        print("starting cycle Nr: ",cycle, " at: ", cycleStart)

        # this is coin adding
        if cycle == 7:

            # checking all coins from coingecko and adding coins to the db that aren't in db
            # checking address for all coins and adding it to coins that have a bsc address
            print("checking for new coins at: ", cycleStart)
            adding_new_coins_to_db()

            # checking coins and those that are younger than 5 mins copy to new_coins table
            # delete coins that are without address
            dateTimeObj = datetime.now()
            print("moving some new coins at: ", dateTimeObj)
            move_new_coins()

            print("reseting cycle to 0")
            cycle = 0
            cycleStart = datetime.now()


        # this is coin selling
        print("checking wallet how many coins at: ", cycleStart)
        updating_wallet()

        dateTimeObj = datetime.now()
        print("checking prices in wallet at: ", dateTimeObj)
        os.system('node wallet_coin_price.js')

        dateTimeObj = datetime.now()
        print("calculating coins at: ", dateTimeObj)
        calculate_wallet()

        dateTimeObj = datetime.now()
        print("selling coins at: ", dateTimeObj)
        os.system('node sell_coins.js')

        dateTimeObj = datetime.now()
        print("checking if coins are sold and if needed fixing decimal: ", dateTimeObj)
        decimal_fixing()


        # this is coin buying
        dateTimeObj = datetime.now()
        print("checking prices for new coins at: ", dateTimeObj)
        os.system('node new_coin_price.js')

        dateTimeObj = datetime.now()
        print("calculating coins at: ", dateTimeObj)
        calculate_new_coins()

        dateTimeObj = datetime.now()
        print("buying new coins at: ", dateTimeObj)
        os.system('node buy_coins.js')



        cycleEnd = datetime.now()
        cycleTime = cycleEnd - cycleStart
        print("cycle time =", cycleTime)


        print("sleeping for 45 seconds at: ", cycleEnd)
        time.sleep(45)  # do work every 45 seconds
        dateTimeObj = datetime.now()
        print("slept for 45 seconds at: ", dateTimeObj)


        # add 1 to the cycle
        cycle +=1


        # space between cycles
        print(" ")
        print(" ")
