const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/nauris/Documents/GitHub/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
});

let sql = `SELECT address coinAddress FROM new_coins`;
let errorCount = 0

db.all(sql, [], (err, rows) => {

  let allCoins = rows

  async function check_pair() {
    for (coin of allCoins) {
      try {

        const ethers = require("ethers");
        
        const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
        const BUSD = coin.coinAddress;
        const router = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73";

        const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=1086c980-0118-4f0e-85dd-67f7172336dd");
        
        const mnemonic = "exercise dumb famous kingdom auto sweet celery position mad angry pioneer record";
        
        const wallet = new ethers.Wallet.fromMnemonic(mnemonic);
        
        const signer = wallet.connect(provider);
        
        const routerContract = new ethers.Contract(
            router,
            [
                'function getPair(address tokenA, address tokenB) external view returns (address pair)'
            ],
            signer
        );

        const gotPair = await routerContract.getPair(WBNB, BUSD)
        response = gotPair
        // console.log(response)

        let sql_pair = `UPDATE new_coins
        SET got_pair = '${response}'
        WHERE address = '${coin.coinAddress}'`;
        db.run(sql_pair,[]);
      } catch (err) {
        // console.log(err)
        // console.log("this is error: ", err.reason)

        let errHistory = `INSERT pair_coin_errors(address, reason, error) VALUES('${coin.coinAddress}','${err.reason}','${err}')`;
        db.run(errHistory,[]);
        
        errorCount ++
        continue;
      }
    }
    console.log("new coin checking got:", errorCount, "errors")
  }
  check_pair();
});
