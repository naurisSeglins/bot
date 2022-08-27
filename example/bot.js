async function buy_coin() {    

    const ethers = require("ethers");

    const WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; 
    const TokenOut = "0x748ed23b57726617069823dc1e6267c8302d4e76";

    const router = "0x10ED43C718714eb63d5aA57B78B54704E256024E";
    
    const recipient = "wallet_address";
    
    const provider = new ethers.providers.JsonRpcProvider("https://bsc.getblock.io/mainnet/?api_key=key");
    
    const mnemonic = "phrase";
    
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

    const WBNBamountIn = ethers.utils.parseUnits("0.01", "ether");
    let amounts = await routerContract.getAmountsOut(WBNBamountIn, [WBNB, TokenOut]);
    const TokenOutamountOutMin = amounts[1].sub(amounts[1].div(10));


    const approveTx = await wbnbContract.approve(
        router,
        WBNBamountIn
    );

    let app_reciept = await approveTx.wait();
    console.log(app_reciept);

    
    const swapTx = await routerContract.swapExactTokensForTokens(
        WBNBamountIn,
        TokenOutamountOutMin,
        [WBNB, TokenOut],
        recipient,
        Date.now() + 1000 * 60 * 10,
        {gasLimit: 350000}
    )

    let receipt = await swapTx.wait();
    console.log(receipt);
}
buy_coin();
