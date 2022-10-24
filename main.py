from datetime import datetime
import time 
import os

from adding_coins_to_db import adding_new_coins_to_db
from calculation import calculate_wallet
from calculation import calculate_new_coins
from new_coins import move_new_coins, clean_new_coins
from my_wallet import updating_wallet
from sell_coins import delete_sell_coins
from suspend_coins import suspending_coins


if __name__ == "__main__":

    dateTimeObj = datetime.now()
    print("first time at: ", dateTimeObj)
    cycle = 1

    time.sleep(6)  # imagine you would like to start work in 6 sec first time
    while True:

        cycleStart = datetime.now()
        print("starting cycle Nr: ",cycle, " at: ", cycleStart)

        # this is coin adding
        if cycle == 2:

            # checking all coins from coingecko and adding coins to the db that aren't in db
            # checking address for all coins and adding it to coins that have a bsc address
            print("checking for new coins at: ", cycleStart)
            adding_new_coins_to_db()

            # checking coins and those that are younger than 5 mins copy to new_coins table
            # delete coins that are without address
            dateTimeObj = datetime.now()
            print("moving new coins at: ", dateTimeObj)
            move_new_coins()

            # checking if coins have a pair A.K.A if they are in pancakeswap
            dateTimeObj = datetime.now()
            print("checking if new coins are on pancake swap at: ", dateTimeObj)
            os.system('node pancake_swap_pair.js')
            
            # delete coins that are without pair
            dateTimeObj = datetime.now()
            print("cleaning new coins at: ", dateTimeObj)
            clean_new_coins()


            print("reseting cycle to 0")
            cycle = 0


        # this is coin selling
        dateTimeObj = datetime.now()
        print("checking wallet how many coins at: ", dateTimeObj)
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
        print("checking if coins are sold and if needs to be deleted: ", dateTimeObj)
        delete_sell_coins()


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

        dateTimeObj = datetime.now()
        print("suspending coins at: ", dateTimeObj)
        suspending_coins()

        cycleEnd = datetime.now()
        cycleTime = cycleEnd - cycleStart
        print("cycle time =", cycleTime)
        
        # add 1 to the cycle
        cycle +=1

        if cycle == 2:
            sleepSecs = 20
        else:
            sleepSecs = 25

        sleepTime = sleepSecs - cycleTime.seconds

        if sleepTime < 5:
            sleepTime = 5
        print(f"sleeping for {sleepTime} seconds at: ", cycleEnd)
        time.sleep(sleepTime)  # do work every 30 seconds
        dateTimeObj = datetime.now()
        print(f"slept for {sleepTime} seconds at: ", dateTimeObj)




        # space between cycles
        print(" ")
        print(" ")
