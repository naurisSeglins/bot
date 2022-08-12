const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/nauris/Documents/GitHub/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the coins database.');
});

let sql = `SELECT amount coinAmount,
                  address coinAddress
            FROM wallet WHERE amount != 0`;


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

      // const provider = new ethers.providers.WebSocketProvider("wss://speedy-nodes-nyc.moralis.io/UfWmbh10KZGckKrcJzJksBKIR8ftxOuWg0VRbtyy/bsc/mainnet/ws");
      // const provider = new ethers.providers.WebSocketProvider("wss://ws-nd-277-117-011.p2pify.com/1d52263f7bf104663499af684793dfcb");
      const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=1086c980-0118-4f0e-85dd-67f7172336dd");


      
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

      const WBNBamountIn = ethers.utils.parseUnits(`${coin.coinAmount}`, "ether");
      const amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, BUSD]);
      const BUSDamountOutMin = amounts[1];

      price = ethers.utils.formatEther(BUSDamountOutMin)
      console.log("this is wallet coin price: ", price)
      let sql_price = `UPDATE wallet
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
