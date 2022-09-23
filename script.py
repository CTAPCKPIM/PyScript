# -*- coding: utf-8 -*-

import requests
import json
import os
import cryptocompare as cc

from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

""" All variables

'load_dotenv()'' - load the configuration from a .env;
'headers' - requesting JSON from the site;
'API' - loading the variable;
'web3' - connecting Web3;
'eth_decimals' - decimals of USDC in ETH network;
"""
load_dotenv()

headers = { 
	'Accepts': 'application/json'
}
# Dotenv variables
API = os.getenv('API_KEY')
INFURA = os.getenv('INFURA_URL')
SECRET = os.getenv('SECRET_KEY')

# Connecting providers
ccobj = cc.cryptocompare._set_api_key_parameter(API)
cg = CoinGeckoAPI()
w3 = Web3(Web3.HTTPProvider(INFURA))
w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
address = '0xf39D262c556aBefFC619847eE0355af42c4d0e91'

eth_decimals = 6

etherscan = 'https://api.etherscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken'

''' ABIs and address of smart contracts(Ethereum network) '''
abi_crv = json.loads('[{"inputs":[{"internalType":"address","name":"_addrCRV","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"addrCRV","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnSymbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_priceUSD","type":"uint256"}],"name":"setPriceInUSD","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
abi_weth = json.loads('[{"inputs":[{"internalType":"address","name":"_addrWETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"addrWETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnSymbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_priceUSD","type":"uint256"}],"name":"setPriceInUSD","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
abi_farm = json.loads('[{"inputs":[{"internalType":"address","name":"_addrFARM","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"addrFARM","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnSymbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_priceUSD","type":"uint256"}],"name":"setPriceInUSD","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

address_crv = '0x6DE6013B8Ea9fA78DB10e7D7e4D9E66668FaFAae'
address_weth = '0x71815DcE02aAb149048e68c1EC777331fC890462'
address_farm = '0xA64e04F3309794A7353894465B3e11D0007115aC'

crv = w3.eth.contract(address=address_crv, abi=abi_crv)
weth = w3.eth.contract(address=address_weth, abi=abi_weth)
farm = w3.eth.contract(address=address_farm, abi=abi_farm)

''' Other ABIs and adress '''

#limit = 0

""" Function for a control price of the gas 'Fantom' network """
def getGasLimit():
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(etherscan)  # for fantom
		data_eth = json.loads(response.text)
		if (data_eth['status'] == '1'):
			return int(float(data_eth['result']['FastGasPrice']) * 1e9)  
		else: return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		return 0

#limit = getGasLimit()
#print('New limit: ', limit)
#print('Type: ', type(limit))

""" Function parsing price of the gas

'data_eth' - api.etherscan.com;
"""
def getGasPrise():
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(etherscan)
		data_eth = json.loads(response.text)
		#import pdb; pdb.set_trace() 
		gas_price = int(float(data_eth['result']['FastGasPrice']) * 1e9)
		#print('Gas price: ', gas_price) 
		#print('Type: ', type(gas_price))
		if (data_eth['status'] == '1'): #and gas_price < limit * 5):  #  for Fantom network
			print('Normal price')
			return gas_price
		#elif(data_eth['status'] == '1' and gas_price > limit * 5):  #  for Fantom network
			#print('Price * 5') 
			#return gas_price * 5
		else: return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		return 0

#price = getGasPrise()
#print('Price of gas: ',price)

""" Function parsing price of the cryptocurrency in USD from 'Cryptocompare'

'currency_eth' - array of crypto currencys(CC)
'data' - converting it to a dictionary;
'price' - turn the USD price into a number with a power of 6;
"""
def priceFromCryptocompare():
	session = Session()
	session.headers.update(headers)
	currency_eth = ['CRV', 'WETH', 'FARM']  
	try:
		''' Ethereum network (USDC 6 decimals)'''
		for i in currency_eth:
			response = session.get('https://min-api.cryptocompare.com/data/price?fsym='+ i +'&tsyms=USD')
			data_eth = json.loads(response.text) 
			price = int(data_eth['USD'] * pow(10, eth_decimals)) 
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(Cryptocompare)')
		return 0

#priceFromCryptocompare()

""" Function parsing price of the cryptocurrency in USD from 'CoinGecko'

'currency_eth' - array of crypto currencys(CG);
'data' - converting it to a dictionary;
'usd_' - the price from JSON;
'price' - turn the USD price into a number with a power of 6;
"""
def priceFromCoinGecko():
	session = Session()
	session.headers.update(headers)
	currency_eth = ['curve-dao-token', 'weth', 'harvest-finance']  
	try:
		''' Ethereum network (USDC 6 decimals)'''
		for i in currency_eth:
			response = session.get('https://api.coingecko.com/api/v3/coins/' + i)
			data_eth = json.loads(response.text)
			usd_ = data_eth['market_data']['current_price']['usd']
			price = int(usd_ * pow(10, eth_decimals)) 
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(CoinGecko)')
		return 0

#priceFromCoinGecko()

def txCRV():
	tx = crv.functions.setPriceInUSD(1).build_transaction({
		'nonce': w3.eth.get_transaction_count(address),
		'chainId': 4,  # rinkeby
		'gasPrice': price,
		'gas': 3000000,  
		})
	signed_tx = w3.eth.account.sign_transaction(tx, private_key=SECRET)
	res = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
	print(w3.toHex(res))
#txCRV()





























''' Function for call smart contracts '''
'''def callSmartContracts():
	crv = w3.eth.contract(address=address_crv, abi=abi_crv)
	weth = w3.eth.contract(address=address_weth, abi=abi_weth)
	farm = w3.eth.contract(address=address_farm, abi=abi_farm)

	addr_crv = crv.functions.addrCRV().call()
	addr_weth = weth.functions.addrWETH().call()
	addr_farm = farm.functions.addrFARM().call()
	
	print(addr_crv)
	print(addr_weth)
	print(addr_farm)

#callSmartContracts()'''

''' Other network '''

