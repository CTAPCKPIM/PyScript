# Python script
---
**PyScript** - we are **parsing** the **price** of tokens, using _CoinGecko_, and _Cryptocompare_, and then with help **transactions**, **setting** prices in _smart contracts_.

[**Link on Smart contracts'**](https://github.com/CTAPCKPIM/Smart-contracts-of-prices.git)

---
## Networks(*testnets*):
**(Ethereum:** *Goerli* **)**
 + CRV - [0x9BA0D124e47DB74c40440Dc297FB4d68e8fF8023](https://goerli.etherscan.io/address/0x9BA0D124e47DB74c40440Dc297FB4d68e8fF8023#code); 
 + WETH - [0x2845c79c4879971c6Ac4810b591cbd36f973EAC6](https://goerli.etherscan.io/address/0x2845c79c4879971c6Ac4810b591cbd36f973EAC6#code);
 + FARM - [0x1e9D1602b3D16b1Ac56703cafdC093B6643621D9](https://goerli.etherscan.io/address/0x1e9D1602b3D16b1Ac56703cafdC093B6643621D9#code);

**(Fantom:** *Testnet* **)**
 + SPIRIT - [0x923b10057dc8C15A7b7c55E84E37a3649e160b77](https://testnet.ftmscan.com/address/0x923b10057dc8C15A7b7c55E84E37a3649e160b77#code);
 + WFTM - [0xc40cE45B9734Ff0891AeA10Bb382D4D2620A2F2F](https://testnet.ftmscan.com/address/0xc40ce45b9734ff0891aea10bb382d4d2620a2f2f#code);
 + YFI - [0xE50dcaDDF5D60AB06679881b5dce724B2995C1a0](https://testnet.ftmscan.com/address/0xE50dcaDDF5D60AB06679881b5dce724B2995C1a0#code);

**(Polygon:** *Mumbai* **)**
 + QUICK - [0x6C7f693fe02b04c9302E16721Cd9680432c0e5A5](https://mumbai.polygonscan.com/address/0x6C7f693fe02b04c9302E16721Cd9680432c0e5A5#code);
 + ORBS - [0x465fBD82c206986B9A1E5eD8943c56Ba898b6501](https://mumbai.polygonscan.com/address/0x465fBD82c206986B9A1E5eD8943c56Ba898b6501#code);
 + WMATIC - [0xdeae7b833d107915dC9F051E81c06E9c12779aC1](https://mumbai.polygonscan.com/address/0xdeae7b833d107915dC9F051E81c06E9c12779aC1#code);

**(AVAX:** *Avalanche Fuji* **)**
 + WAVAX - [0x3548117307121f582270Aae03AC334B3E26756c3](https://testnet.snowtrace.io/address/0x3548117307121f582270Aae03AC334B3E26756c3#code);
 + SPELL - [0x66aEe73703011bcCD46a66E2F994dCA13925c539](https://testnet.snowtrace.io/address/0x66aEe73703011bcCD46a66E2F994dCA13925c539#code);
 + PTP - [0x789DebCE62D5F3F38Aa973135b96BaE4b3Cf8a80](https://testnet.snowtrace.io/address/0x789DebCE62D5F3F38Aa973135b96BaE4b3Cf8a80#code);

**(BSC:** *Testnet* **)**
 + WBNB - [0x3E5B7EbA31224Dfc573d20081f30395aF295a43b](https://testnet.bscscan.com/address/0x3E5B7EbA31224Dfc573d20081f30395aF295a43b#code);
 + CAKE - [0x6187746e4FC586002e0D3134f944505C34FbD4AE](https://testnet.bscscan.com/address/0x6187746e4FC586002e0D3134f944505C34FbD4AE#code); 
 + STG - [0xAC125837E0885C218E1012177beFdC257f01b2d2](https://testnet.bscscan.com/address/0xAC125837E0885C218E1012177beFdC257f01b2d2#code);
 
___
## Hint:

>  Don't forget to add the keys in  _.env_ and _APIs.json_ 

__To work this script you must:__
1. __Two__ your keys in _.env_:
    + __First__ - for a signature of the transaction(_take in MetaMask_)
    + __Second__ - for connecting to _Cryptocompare_
    `SECRET_KEY = <first key>`
    `API_KEY = <second key>`
2. __Ten__ your keys in _APIs.json_:
    + 5/4002/80001/43113/97 - _chains id's_
    ```
    {
	"net": "Ethereum_",
	"5": <API key of the provider(infura)>,
	<API key of the provider(infura)>: <key from etherscan>,
	
	"net": "Fantom_",
	"4002": <API key of the provider(blastapi)>,
	<API key of the provider(blastapi)>: <key from ftmscan>,

	"net": "Mumbai_",
	"80001": <API key of the provider(alchemy)>,
	<API key of the provider(alchemy)>: <key from polygonscan>,

	"net": "AVAX_",
	"43113": <API key of the provider(infura)>,
	<API key of the provider(infura)>: <key from snowtrace>,

	"net": "BSC_",
	"97": <API key of the provider(quiknode)>,
	<API key of the provider(quiknode)>: <key from bscscan>"
    }
    ```