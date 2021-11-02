const ethers = require("ethers");
var dateFormat = require("dateformat");

const addresses = {
  WBNB: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
  elonDoge: "0xf01830e8642a33e8cff5550d986d1031601c9f1a",
  safeMoon: "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3",
  //<-- šeit adresi -->
  factory: "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
  router: "0x10ED43C718714eb63d5aA57B78B54704E256024E",

  recipient: "0x73625badDA7Dfa52bDBf0340Ae688c2E89bB21E6",
};

const mnemonic =
  "summer ugly motor speed rail awake gate ripple arm ugly task siren";

const provider = new ethers.providers.WebSocketProvider(
  "wss://bsc-ws-node.nariox.org:443"
);

const wallet = ethers.Wallet.fromMnemonic(mnemonic);

const account = wallet.connect(provider);

const factory = new ethers.Contract(
  addresses.factory,
  [
    "event PairCreated(address indexed token0, address indexed token1, address pair, uint)",
  ],

  account
);
const router = new ethers.Contract(
  addresses.router,
  [
    "function getAmountsOut(uint amountIn, address[] memory path) public view returns (uint[] memory amounts)",
    "function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts)",
  ],
  account
);

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

//timeris
let timer = setInterval(function () {
  var day = dateFormat(new Date(), "yyyy-mm-dd h:MM:ss");
  console.log(`
    Time
    =================
    date: ${day}
  `);
  buyToken();
}, 5000); //seconds /1000

buyToken();

//galvenā funkcija
async function buyToken() {
  var day = dateFormat(new Date(), "yyyy-mm-dd h:MM:ss");
  //<-- šeit adresi -->
  console.log(`
    Token to buy and sell
    =================
    tokenIn: ${addresses.WBNB}
    tokenOut: ${addresses.elonDoge}
    date: ${day}
  `);

  //WBNB
  let tokenIn = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c";
  // ElonDoge
  let tokenOut = "0xf01830e8642a33e8cff5550d986d1031601c9f1a";
  //Safemoon
  // let tokenOut = "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3";
  //<-- šeit adresi -->

  if (tokenIn === addresses.WBNB) {
    console.log("tokenIn === addresses.WBNB");
  }
  if (tokenOut === addresses.elonDoge) {
    console.log("tokenOut === addresses.ElonDoge");
  }
  // if (tokenOut === addresses.safeMoon) {
  //   console.log("tokenOut === addresses.SafeMoon");
  // }
  if (typeof tokenIn === "undefined") {
    console.log("something is wrong with tokeIn");
    return;
  }

  const amountIn = ethers.utils.parseUnits("0.002", "ether");

  const amounts = await router.getAmountsOut(amountIn, [tokenIn, tokenOut]);

  const amountOutMin = amounts[1].sub(amounts[1].div(20));
  var day = dateFormat(new Date(), "yyyy-mm-dd h:MM:ss");

  console.log(`
      Gonna buy new token
      =================
      tokenIn: ${ethers.utils.formatEther(amountIn)} ${tokenIn} (WBNB)
      tokenOut: ${amountOutMin.toString()} ${tokenOut} (elonDoge)
      date: ${day}
    `);


// *************************** pirkšanas funkcija ************************************
  //<-- šeit adresi -->
  // if (tokenOut == "0xf01830e8642a33e8cff5550d986d1031601c9f1a") {
  //   var day = dateFormat(new Date(), "yyyy-mm-dd h:MM:ss");
  //   console.log(`
  //   The right token
  //   =================
  //   tokenOut: ${tokenOut}
  //   date: ${day}
  // `);
  //   const tx = await router.swapExactTokensForTokens(
  //     amountIn,

  //     amountOutMin,

  //     [tokenIn, tokenOut],

  //     addresses.recipient,

  //     Date.now() + 1000 * 60 * 10
  //   );
  //   clearInterval(timer);
  // } else {
  //   console.log("Waiting for the right token");
  // }
  // const receipt = await tx.wait();
  // console.log("Transaction receipt");
  // console.log(receipt);
}

init();
