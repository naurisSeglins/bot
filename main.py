from datetime import datetime
import time 
import os

from adding_coins_to_db import do_some_work
from moving_new_coins import move_some_coins
from my_wallet import checking_wallet


if __name__ == "__main__":

    dateTimeObj = datetime.now()
    print("first time at: ", dateTimeObj)

    time.sleep(6)  # imagine you would like to start work in 6 sec first time
    while True:

        dateTimeObj = datetime.now()
        print("doing the work at: ", dateTimeObj)

        do_some_work()

        dateTimeObj = datetime.now()
        print("moving some new coins at: ", dateTimeObj)

        move_some_coins()
        
        dateTimeObj = datetime.now()
        print("moving new coins to wallet at: ", dateTimeObj)

        checking_wallet()

        dateTimeObj = datetime.now()
        print("checking prices in wallet at: ", dateTimeObj)

        os.system('node wallet_coin_price.js')

        os.system('node disconnect_to_db.js')

        # dateTimeObj = datetime.now()
        # print("buying new coins at: ", dateTimeObj)

        # os.system('node buy_coins.js')
        # os.system('node sell_coins_git_yt.js')


        dateTimeObj = datetime.now()
        print("sleeping for 5 minutes at: ", dateTimeObj)

        time.sleep(300)  # do work every one hour

        dateTimeObj = datetime.now()
        print("slept for 5 minutes at: ", dateTimeObj)

        