// ************************* VARIABLES ***********************************

const ethers = require('ethers');

const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
const BUSD = "0xe9e7cea3dedca5984780bafc599bd69add087d56";

const pair = "0x1B96B92314C44b159149f7E0303511fB2Fc4774f";

// const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";
const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";


// const mnemonic = "summer ugly motor speed rail awake gate ripple arm ugly task siren";
const privatekey = "3f315ad2762ec83147f62390c1a0a1f41a7210ac35437340a83728b1baa12b73"
const provider = new ethers.providers.WebSocketProvider(
    "wss://bsc-ws-node.nariox.org:443"
);

// const wallet = ethers.Wallet.fromMnemonic(mnemonic);
const wallet = new ethers.Wallet(privatekey);

const signer = wallet.connect(provider);

// ************************* CONTRACTS ***********************************

const pairContract = new ethers.Contract(
    pair,
    [
      "event Swap(address indexed sender, uint amount0In, uint amount1In, uint amount0Out, uint amount1Out, address indexed to)",
      "function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast)"
    ],
    signer
);

const routerContract = new ethers.Contract(
    router,
    [
        'function getAmountsOut(uint amountIn, address[] memory path) public view returns(uint[] memory amounts)',
        'function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts)'
    ],
    signer
);

// ************************* LOGIC ***********************************
const asyncMiddleware = fn =>
  (req, res, next) => {
    Promise.resolve(fn(req, res, next))
      .catch(next);
  };

pairContract.on("Swap", async (req, res, next) => {
    try {
        console.log("Swap happened, considering trade...");

        const pairData = await pairContract.getReserves();
        const bnbReserve = ethers.utils.formatUnits(pairData[0], 18);
        const usdReserve = ethers.utils.formatUnits(pairData[1], 18);
        const conversion = Number(usdReserve) / Number(bnbReserve);

        console.log(`
        BlockTimestamp: ${pairData[2]}
        WBNB Reserve: ${bnbReserve}
        BUSD Reserve: ${usdReserve}
        WBNB Price: ${conversion}
        `);
        next();
    } catch (error) {
        next(error);
    }
});