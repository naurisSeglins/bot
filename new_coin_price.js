const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('/home/nauris/Documents/GitHub/bot/coins.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
});

let sql = `SELECT address coinAddress FROM new_coins`;


db.all(sql, [], (err, rows) => {

  let allCoins = rows

  async function check_price() {
    for (coin of allCoins) {
      try {

        const ethers = require("ethers");
        
        const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
        const BUSD = coin.coinAddress;
        const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";

        // const provider = new ethers.providers.WebSocketProvider("wss://speedy-nodes-nyc.moralis.io/a38b817304311265560d67b7/bsc/mainnet/ws");
        const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=1086c980-0118-4f0e-85dd-67f7172336dd");
        // const provider = new ethers.providers.WebSocketProvider("wss://ws-nd-277-117-011.p2pify.com/1d52263f7bf104663499af684793dfcb");
        
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
        // console.log("this is address: ", BUSD)
        const WBNBamountIn = ethers.utils.parseUnits("0.01", "ether");
        const amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, BUSD]);
        const BUSDamountOutMin = amounts[1];

        price = ethers.utils.formatEther(BUSDamountOutMin)
        // console.log("this is price: ", price)
        // console.log("this is new coin price: ", price)
        let sql_price = `UPDATE new_coins
        SET bnb_price = ${price}
        WHERE address = '${coin.coinAddress}'`;
        db.run(sql_price,[]);
      } catch (err) {
        console.log("this is error: ", err.reason)
        // nepieciešams skaits cik reizes coinam ir izmests errors !!!!!

        // continue ir vajadzīgs lai pie errora programma neapstātos, bet turpinātu strādāt tālāk
        continue;
      }
    }
  }
  check_price();
});

// function close_script(){
//   db.close((err) => {
//     if (err) {
//       console.error(err.message);
//     }
//     console.log('Close the database connection.');
//   });
//   process.exit()
// }

// setTimeout(close_script, 10000);
