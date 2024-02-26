const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/bot/Desktop/bot/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
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
        
        const recipient = "";
        
        const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=");
        
        const mnemonic = "";
        
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
        let gasLimit = 1000000
        if (coin.dbErrorCount == 1){
          slippage = 5
          gasLimit = 1500000
        }
        if (coin.dbErrorCount == 2){
          slippage = 3
          gasLimit = 2000000
        }
        console.log("main buy function is called");
        const WBNBamountIn = ethers.utils.parseUnits("0.02", "ether");
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
          {gasLimit: gasLimit}
        )

        let receipt = await swapTx.wait();
        let trxHash  = String(receipt.transactionHash)
        let trx_status = receipt.status
        console.log(trx_status)
        let sql_bought = `INSERT INTO bought_trx_history(hash, id, address, status) VALUES('${trxHash}','${coin.coinId}','${coin.coinAddress}',${trx_status})`;
        db.run(sql_bought,[]);

      
      // catch (err) ir nepieciešams, lai zem err tiktu saglabāts error response
      } catch (err) {
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
