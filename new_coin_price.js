const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/nauris/Documents/GitHub/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  // console.log('Connected to the coins database.');
});

// let sql = `SELECT amount coinAmount,
//                   address coinAddress
//             FROM wallet WHERE amount != 0`;

let sql = `SELECT address coinAddress,
                  id coinId
            FROM coins_on_scanner`;

db.each(sql, [], (err, row) => {
  if (err) {
    throw err;
  }
  // console.log(`
  // ${row.coinAmount} - ${row.coinAddress}`);

  const ethers = require("ethers");
  var dateFormat = require("dateformat");
  
  const BUSD = "0xe9e7cea3dedca5984780bafc599bd69add087d56"; 
  // const BUSD = row.coinAddress;
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
  
    // 1 coin
      const CoinamountIn = ethers.utils.parseUnits("1", "ether");
      // 1  coin is worth how much BUSD ?
      let amounts = await routerContract.getAmountsOut(CoinamountIn, [WBNB, BUSD]);
      const BUSDAmountOutMin = amounts[1];
  
      console.log(ethers.utils.formatEther(CoinamountIn));
      console.log(ethers.utils.formatEther(BUSDAmountOutMin));


      price = ethers.utils.formatEther(BUSDAmountOutMin)
      column_name = row.coinId
      column_name = column_name.replace(/-/g, '_')
      console.log(row.coinId)
      console.log(column_name)
      let sql_price = `INSERT INTO coin_watcher(${column_name}) VALUES(${price})`;

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

