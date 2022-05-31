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

  const addresses = {
    WBNB: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    new_coin: row.coinAddress,
    //<-- šeit adresi -->
    factory: "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
    router: "0x10ED43C718714eb63d5aA57B78B54704E256024E",
    recipient: "0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59",
  };

  const mnemonic =
    "exercise dumb famous kingdom auto sweet celery position mad angry pioneer record";

  const provider = new ethers.providers.WebSocketProvider(
    "wss://bsc-ws-node.nariox.org:443"
  );

  const wallet = ethers.Wallet.fromMnemonic(mnemonic);

  const account = wallet.connect(provider);

// ************************* CONTRACTS ***********************************

  const router = new ethers.Contract(
    addresses.router,
    [
      "function getAmountsOut(uint amountIn, address[] memory path) public view returns (uint[] memory amounts)",
      "function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts)",
    ],
    account
  );

// ************************* LOGIC ***********************************

  //Approve some Wrapped BNB to be spent by the PancakeSwap router

  const WBNB = new ethers.Contract(
    addresses.WBNB,
    ["function approve(address spender, uint amount) public returns(bool)"],
    account
  );

  const valueToapprove = ethers.utils.parseUnits("0.05", "ether");
  const init = async () => {
    const tx = await WBNB.approve(router.address, valueToapprove);
    const receipt = await tx.wait();
    console.log("Transaction receipt");
    console.log(receipt);
  };

  buyToken();


  //galvenā funkcija
  async function buyToken() {
    var day = dateFormat(new Date(), "yyyy-mm-dd h:MM:ss");
    //<-- šeit adresi -->
    console.log(`
      Token to buy and sell
      =================
      tokenIn: ${addresses.WBNB}
      tokenOut: ${addresses.new_coin}
      date: ${day}
    `);

    //WBNB
    let tokenIn = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c";
    // New coin
    let tokenOut = addresses.new_coin;

    if (tokenIn === addresses.WBNB) {
    }
    if (tokenOut === addresses.new_coin) {
    }
    if (typeof tokenIn === "undefined") {
      console.log("something is wrong with tokeIn");
      return;
    }

    const amountIn = ethers.utils.parseUnits("0.005", "ether");

    const amounts = await router.getAmountsOut(amountIn, [tokenIn, tokenOut]);

    const amountOutMin = amounts[1].sub(amounts[1].div(10));
    var day = dateFormat(new Date(), "yyyy-mm-dd h:MM:ss");

    console.log(`
        Gonna buy new token
        =================
        tokenIn: ${ethers.utils.formatEther(amountIn)} ${tokenIn} (WBNB)
        tokenOut: ${ethers.utils.formatEther(amountOutMin)} ${row.coinId}
        date: ${day}
      `);

  // *************************** pirkšanas funkcija ************************************
    //   const tx = await router.swapExactTokensForTokens(
    //     amountIn,

    //     amountOutMin,

    //     [tokenIn, tokenOut],

    //     addresses.recipient,

    //     Date.now() + 1000 * 60 * 10,

    //     {gasLimit: 250000}

    //   );
    // const receipt = await tx.wait();
    // console.log("Transaction receipt");
    // console.log(receipt);
  }

  init();
});

db.close((err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Close the database connection.');
});









