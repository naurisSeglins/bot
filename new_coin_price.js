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

// let sql = `SELECT address coinAddress,
//             FROM coin_watcher`;

// db.each(sql, [], (err, row) => {
  // if (err) {
  //   throw err;
  // }
  // console.log(`
  // ${row.coinAmount} - ${row.coinAddress}`);

  const ethers = require("ethers");
  var dateFormat = require("dateformat");
  
  const BUSD = "0xe9e7cea3dedca5984780bafc599bd69add087d56"; 
  // const WBNB = row.coinAddress;
  const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c";

  
  const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";

  // const provider = new ethers.providers.WebSocketProvider("wss://bsc-ws-node.nariox.org:443");

  const provider = new ethers.providers.WebSocketProvider("wss://speedy-nodes-nyc.moralis.io/a38b817304311265560d67b7/bsc/mainnet/ws");

  // const provider = new ethers.providers.JsonRpcProvider("https://eth-mainnet.alchemyapi.io/v2/BgkSpGyt8kRdRNvwgKoXRSpemF_EO6kl");
  
  const mnemonic = "exercise dumb famous kingdom auto sweet celery position mad angry pioneer record";
  
  // const wallet = new ethers.Wallet(privatekey);
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
  
      const WBNBamountIn = ethers.utils.parseUnits("1", "ether");
      let amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, BUSD]);
      const BUSDamountOutMin = amounts[1];
  
      console.log(ethers.utils.formatEther(WBNBamountIn));
      console.log(ethers.utils.formatEther(BUSDamountOutMin));


      // price = ethers.utils.formatEther(BUSDamountOutMin)
      // let sql_price = `UPDATE wallet
      // SET bnb_price = ${price}
      // WHERE address = '${row.coinAddress}'`;
    
      // db.run(sql_price,[]);
  }
  
  check_price();
// });



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

