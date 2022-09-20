const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/bot/Desktop/bot/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
});

let sql = `SELECT id coinId,
                  address coinAddress,
                  amount coinAmount,
                  decimal decimal
            FROM sell_coins`;  
let errorCount = 0

db.all(sql, [], (err, rows) => {

  let allCoins = rows
  async function sell_coin() {    

    for (coin of allCoins) {
      console.log("there is a coin to sell")
      try {

        const ethers = require("ethers");
      
        const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
        const BUSD = coin.coinAddress;
        
        const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";
        
        const recipient = "0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59";
        
        // const provider = new ethers.providers.WebSocketProvider("wss://bsc-ws-node.nariox.org:443");
        const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=1086c980-0118-4f0e-85dd-67f7172336dd");
        // const provider = new ethers.providers.WebSocketProvider("wss://ws-nd-277-117-011.p2pify.com/1d52263f7bf104663499af684793dfcb");

        
        const mnemonic = "exercise dumb famous kingdom auto sweet celery position mad angry pioneer record";
        
        // const wallet = new ethers.Wallet(privatekey);
        const wallet = new ethers.Wallet.fromMnemonic(mnemonic);
        
        const signer = wallet.connect(provider);
        
        const routerContract = new ethers.Contract(
          router,
          [
            'function getAmountsOut(uint amountIn, address[] memory path) public view returns (uint[] memory amounts)',
            'function swapExactTokensForETHSupportingFeeOnTransferTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts)'
          ],
          signer
        );
        // nav skaidrs par šo funkciju vai ir jāmaina WBNB uz coinu adresi vai arī jāatstāj WBNB
        // Mēģināšu samainīt WBNB uz BUSD jo kad funkcija tiek izsaukta kā parametrs tiek likts BUSD
        const wbnbContract = new ethers.Contract(
          WBNB,
          [
            'function approve(address spender, uint256 amount) external returns (bool)'
          ],
          signer
        )

        console.log("main sell function is called");
        // šeit ar amount varētu būt problēma!!!!
        console.log(coin.coinAddress)
        // if the coin decimal is 9 then have to multiple by this number = 1000000000
        // if the coin decimal is 18 then have to multiple by this number = 1000000000000000000
        let multiplier = 1000000000000000000
        if (coin.decimal == 9){
          multiplier = 1000000000
        }

        let amount = coin.coinAmount * multiplier
        const BUSDamountIn = ethers.utils.parseUnits(`${amount}`, coin.decimal);

        let amounts = await routerContract.getAmountsOut(BUSDamountIn, [BUSD, WBNB]);
        const WBNBamountOutMin = amounts[1].sub(amounts[1].div(10));
    
        const approveTx = await wbnbContract.approve(
          router,
          BUSDamountIn
        );
        let app_reciept = await approveTx.wait();
        console.log("this is approve receipt status: ", app_reciept.status)
        let appHash  = String(app_reciept.transactionHash)
        let app_status = app_reciept.status
        let sql_approve = `INSERT INTO sold_trx_approve(hash, status) VALUES('${appHash}', ${app_status})`;
        db.run(sql_approve,[]);


        const swapTx = await routerContract.swapExactTokensForETHSupportingFeeOnTransferTokens(
          BUSDamountIn,
          WBNBamountOutMin,
          [BUSD, WBNB],
          recipient,
          Date.now() + 1000 * 60 * 10,
          {gasLimit: 1000000}
        )

        let receipt = await swapTx.wait();
        console.log("this is sell trx status: ",receipt.status);

        let trxHash  = String(receipt.transactionHash)
        let trx_status = receipt.status

        let sql_bought = `INSERT INTO sold_trx_history(hash, id, address, status) VALUES('${trxHash}','${coin.coinId}','${coin.coinAddress}',${trx_status})`;
        db.run(sql_bought,[]);
        let sell_coins_table = `UPDATE sell_coins SET status = ${trx_status} WHERE address = '${coin.coinAddress}'`;
        db.run(sell_coins_table,[]);

      // catch (err) ir nepieciešams, lai zem err tiktu saglabāts error response
      } catch (err) {
        // console.log("this is sell trx error status: ", err.receipt.status)
        let trxHash  = String(err.receipt.transactionHash)
        let trx_status = err.receipt.status
        let sql_sell = `INSERT INTO sold_trx_history(hash, id, address, status) VALUES('${trxHash}','${coin.coinId}','${coin.coinAddress}',${trx_status})`;
        db.run(sql_sell,[]);

        // šeit tiek paņemts errora receipt status kurš ir 0 un pievienots sell_table table
        let sell_coins_table = `UPDATE sell_coins SET status = ${trx_status} WHERE address = '${coin.coinAddress}'`;
        db.run(sell_coins_table,[]);


        let errHistory = `INSERT sell_coin_errors(address, reason, error) VALUES('${coin.coinAddress}','${err.reason}','${err}')`;
        db.run(errHistory,[]);
        // nepieciešams skaits cik reizes coinam ir izmests errors !!!!!

        errorCount ++
        // continue ir vajadzīgs lai pie errora programma neapstātos, bet turpinātu strādāt tālāk
        continue;
      }
    }
    console.log("sell coin got:", errorCount, "errors")
  }
  sell_coin();
});
