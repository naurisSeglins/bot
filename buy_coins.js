const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/nauris/Documents/GitHub/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the coins database.');
});

let sql = `SELECT id coinId,
                  address coinAddress
            FROM new_coins`;

db.each(sql, [], (err, row) => {
  if (err) {
    throw err;
  }
  console.log(`
  ${row.coinId} - ${row.coinAddress}`);
  const ethers = require("ethers");
  var dateFormat = require("dateformat");
  // const privatekey = "3abfee713b4d1d61608b6d2426129560879ea89298a05b8e46ae09a9613fbcfa"
  
  const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
  const BUSD = row.coinAddress;
  
  const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";
  
  const recipient = "0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59";
  
  const provider = new ethers.providers.WebSocketProvider("wss://bsc-ws-node.nariox.org:443");
  
  const mnemonic = "exercise dumb famous kingdom auto sweet celery position mad angry pioneer record";
  
  // const wallet = new ethers.Wallet(privatekey);
  const wallet = new ethers.Wallet.fromMnemonic(mnemonic);
  
  const signer = wallet.connect(provider);
  
  
  const routerContract = new ethers.Contract(
      router,
      [
          'function getAmountsOut(uint amountIn, address[] memory path) public view returns (uint[] memory amounts)',
          'function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts)'
      ],
      signer
  );
  
  const wbnbContract = new ethers.Contract(
      WBNB,
      [
          'function approve(address spender, uint256 amount) external returns (bool)'
      ],
      signer
  )
  
  async function main() {
  
      const WBNBamountIn = ethers.utils.parseUnits("0.005", "ether");
      let amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, BUSD]);
      const BUSDamountOutMin = amounts[1].sub(amounts[1].div(10));
  
      console.log(ethers.utils.formatEther(WBNBamountIn));
      console.log(ethers.utils.formatEther(BUSDamountOutMin));
  
      // const approveTx = await wbnbContract.approve(
      //     router,
      //     WBNBamountIn
      // );
      // let reciept = await approveTx.wait();
      // console.log(reciept);
  
      // const swapTx = await routerContract.swapExactTokensForTokens(
      //     WBNBamountIn,
      //     BUSDamountOutMin,
      //     [WBNB, BUSD],
      //     recipient,
      //     Date.now() + 1000 * 60 * 10,
      //     {gasLimit: 250000}
      // )
  
      // receipt = await swapTx.wait();
      // console.log(receipt);
  }
  
  main().then().finally(() => {});
});
db.close((err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Close the database connection.');
});










