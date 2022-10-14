const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/bot/Desktop/bot/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the coins database.');
});

let sql = `SELECT id coinId,
                  address coinAddress,
                  error_count dbErrorCount
            FROM buy_coins`;

let errorCount = 0

db.all(sql, [], (err, rows) => {

  if (err) {
    console.log(err)
  }

  let allCoins = rows
  async function buy_coin() {    

    for (coin of allCoins) {
      console.log("there is a coin to buy")
      try {

        console.log(coin)

        const ethers = require("ethers");
      
        const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
        const TokenOut = coin.coinAddress;

        
        const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";
        
        const recipient = "0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59";
        
        const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=1086c980-0118-4f0e-85dd-67f7172336dd");
        // const provider = new ethers.providers.WebSocketProvider('wss://ws-nd-277-117-011.p2pify.com/1d52263f7bf104663499af684793dfcb', 56);

        
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
        let slippage = 10
        if (coin.dbErrorCount == 1){
          slippage = 5
        }
        if (coin.dbErrorCount == 2){
          slippage = 3
        }
        console.log("main buy function is called");
        const WBNBamountIn = ethers.utils.parseUnits("0.005", "ether");
        let amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, TokenOut]);
        const TokenOutamountOutMin = amounts[1].sub(amounts[1].div(slippage));
    
        console.log("prices")
        console.log(ethers.utils.formatEther(WBNBamountIn));
        console.log(ethers.utils.formatEther(TokenOutamountOutMin));
    
        const approveTx = await wbnbContract.approve(
            router,
            WBNBamountIn
        );
        let app_reciept = await approveTx.wait();
        // console.log(app_reciept);
        let appHash  = String(app_reciept.transactionHash)
        let app_status = app_reciept.status
        let sql_approve = `INSERT INTO bought_trx_approve(hash, status) VALUES('${appHash}', ${app_status})`;
        db.run(sql_approve,[]);
        
        const swapTx = await routerContract.swapExactTokensForTokens(
          WBNBamountIn,
          TokenOutamountOutMin,
          [WBNB, TokenOut],
          recipient,
          Date.now() + 1000 * 60 * 10,
          {gasLimit: 1000000}
        )

        let receipt = await swapTx.wait();
        // console.log(receipt);
        // console.log(receipt.transactionHash);
        // console.log(receipt.status);
        let trxHash  = String(receipt.transactionHash)
        let trx_status = receipt.status
        // console.log(trxHash);
        console.log(trx_status)
        let sql_bought = `INSERT INTO bought_trx_history(hash, id, address, status) VALUES('${trxHash}','${coin.coinId}','${coin.coinAddress}',${trx_status})`;
        db.run(sql_bought,[]);

      
      // catch (err) ir nepieciešams, lai zem err tiktu saglabāts error response
      } catch (err) {
        // console.log("this is buy trx error status: ", err.receipt.status)
        let trxHash  = String(err.receipt.transactionHash)
        let trx_status = err.receipt.status
        let sql_bought = `INSERT OR IGNORE INTO bought_trx_history(hash, id, address, status) VALUES('${trxHash}','${coin.coinId}','${coin.coinAddress}',${trx_status})`;
        db.run(sql_bought,[]);

        coin.dbErrorCount ++
        let buy_coins_error_count = `UPDATE buy_coins SET error_count = ${coin.dbErrorCount} WHERE address = '${coin.coinAddress}'`;
        db.run(buy_coins_error_count,[]);

        let errHistory = `INSERT INTO buy_coin_errors(address, error) VALUES('${coin.coinAddress}','${err}')`;
        db.run(errHistory,[]);
        // continue ir vajadzīgs lai pie errora programma neapstātos, bet turpinātu strādāt tālāk
        errorCount ++
        continue;
      }
    }
    console.log("buy coin got:", errorCount, "errors")
  }
  buy_coin();

});
