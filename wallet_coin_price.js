const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/bot/Desktop/bot/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
});

let sql = `SELECT amount coinAmount,
                  address coinAddress,
                  decimal coinDecimal
            FROM wallet WHERE amount != 0`;

let errorCount = 0

db.all(sql, [], (err, rows) => {
  if (err) {
    throw err;
  }
  let allCoins = rows

  async function check_price() {
    for (coin of allCoins) {
      try{
        const ethers = require("ethers");
        
        const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
        const token = coin.coinAddress;
        const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";
        const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=");

        const mnemonic = "";
        
        const wallet = new ethers.Wallet.fromMnemonic(mnemonic);
        
        const signer = wallet.connect(provider);
        
        const routerContract = new ethers.Contract(
            router,
            [
                'function getAmountsOut(uint amountIn, address[] memory path) public view returns (uint[] memory amounts)',
            ],
            signer
        );

        const TokenAmountIn = ethers.utils.parseUnits(`${coin.coinAmount}`, coin.coinDecimal);
        const amounts = await routerContract.getAmountsOut(TokenAmountIn, [token, WBNB]);
        const WBNBamountOutMin = amounts[1];

        price = ethers.utils.formatEther(WBNBamountOutMin)
        let sql_price = `UPDATE wallet
        SET bnb_price = ${price}
        WHERE address = '${coin.coinAddress}'`;
        db.run(sql_price,[]);
      } catch (err) {
        let errHistory = `INSERT INTO wallet_coin_errors(address, error) VALUES('${coin.coinAddress}','${err}')`;
        db.run(errHistory,[]);
        // continue ir vajadzīgs lai pie errora programma neapstātos, bet turpinātu strādāt tālāk

        errorCount ++
        continue;
      }
    }
    console.log("wallet coin checking got:", errorCount, "errors")
  }
  check_price();
});

function close_script(){
  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Close the database connection.');
  });
  process.exit()
}

setTimeout(close_script, 5000);
