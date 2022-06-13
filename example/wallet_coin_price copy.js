const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/nauris/Documents/GitHub/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  // console.log('Connected to the coins database.');
});

let sql = `SELECT amount coinAmount,
                  address coinAddress
            FROM wallet WHERE amount != 0`;

db.each(sql, [], (err, row) => {
  if (err) {
    throw err;
  }

  const ethers = require("ethers");
  
  const BUSD = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
  const WBNB = row.coinAddress;
  
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

  async function check_price() {
  
      const WBNBamountIn = ethers.utils.parseUnits(`${row.coinAmount}`, "ether");
      let amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, BUSD]);
      // const BUSDamountOutMin = amounts[1].sub(amounts[1].div(10));
      const BUSDamountOutMin = amounts[1];


      price = ethers.utils.formatEther(BUSDamountOutMin)
      // console.log(price)
      // console.log(row.coinAddress)
      let sql_price = `UPDATE wallet
      SET bnb_price = ${price}
      WHERE address = '${row.coinAddress}'`;
    
      db.run(sql_price,[]);
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

