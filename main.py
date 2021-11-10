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

        checking_wallet()

        os.system('node wallet_coin_price.js')

        os.system('node disconnect_to_db.js')


        # dateTimeObj = datetime.now()
        # print("buy some new coins at: ", dateTimeObj)

        # os.system('node buy_coins.js')
        # os.system('node sell_coins_git_yt.js')


        dateTimeObj = datetime.now()
        print("sleeping for 10 minutes at: ", dateTimeObj)

        time.sleep(600)  # do work every one hour

        dateTimeObj = datetime.now()
        print("slept for 10 minutes at: ", dateTimeObj)

        