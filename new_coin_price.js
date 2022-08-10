const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/nauris/Documents/GitHub/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the coins database.');
});

let sql = `SELECT address coinAddress FROM new_coins`;


db.all(sql, [], (err, rows) => {
  if (err) {
    throw err;
  }
  let allCoins = rows

  async function check_price() {
    for (coin of allCoins) {

      const ethers = require("ethers");
      
      const BUSD = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
      const WBNB = coin.coinAddress;
      const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";

      const provider = new ethers.providers.WebSocketProvider("wss://speedy-nodes-nyc.moralis.io/a38b817304311265560d67b7/bsc/mainnet/ws");
      
      const mnemonic = "exercise dumb famous kingdom auto sweet celery position mad angry pioneer record";
      
      const wallet = new ethers.Wallet.fromMnemonic(mnemonic);
      
      const signer = wallet.connect(provider);
      
      const routerContract = new ethers.Contract(
          router,
          [
              'function getAmountsOut(uint amountIn, address[] memory path) public view returns (uint[] memory amounts)',
          ],
          signer
      );

      const WBNBamountIn = ethers.utils.parseUnits("0.01", "ether");
      const amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, BUSD]);
      const BUSDamountOutMin = amounts[1];

      price = ethers.utils.formatEther(BUSDamountOutMin)
      let sql_price = `UPDATE new_coins
      SET bnb_price = ${price}
      WHERE address = '${coin.coinAddress}'`;
      db.run(sql_price,[]);
    }
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
