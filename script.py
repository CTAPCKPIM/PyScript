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
'INFURA' - your address of the provider; 
'SECRET' - your private key;
'w3' - connecting Web3;
'eth_decimals' - decimals of USDC in ETH network;
'eth_price_cc' - the array with price in USD(Cryptocompare);
'eth_price_cg' - the array with price in USD(CoinGecko);
"""
load_dotenv()
with open('dataset.json') as f:
    data = json.load(f)

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

# Variables for decimals 
eth_decimals = 6
address = '0xf39D262c556aBefFC619847eE0355af42c4d0e91'

""" ABIs and address of smart contracts(Ethereum network) """
abi_crv = json.loads('[{"inputs":[{"internalType":"address","name":"_addrCRV","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"addrCRV","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnSymbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_priceUSD","type":"uint256"}],"name":"setPriceInUSD","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
abi_weth = json.loads('[{"inputs":[{"internalType":"address","name":"_addrWETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"addrWETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnSymbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_priceUSD","type":"uint256"}],"name":"setPriceInUSD","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
abi_farm = json.loads('[{"inputs":[{"internalType":"address","name":"_addrFARM","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"addrFARM","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"returnSymbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_priceUSD","type":"uint256"}],"name":"setPriceInUSD","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
# Address`s
address_crv = '0x6DE6013B8Ea9fA78DB10e7D7e4D9E66668FaFAae'
address_weth = '0x71815DcE02aAb149048e68c1EC777331fC890462'
address_farm = '0xA64e04F3309794A7353894465B3e11D0007115aC'

""" Connecting to smart contracts (ETH) """
#crv = w3.eth.contract(address=address_crv, abi=abi_crv)
#weth = w3.eth.contract(address=address_weth, abi=abi_weth)
#farm = w3.eth.contract(address=address_farm, abi=abi_farm)

""" Function parsing price of the gas

'data' - JSON from scans; 
'gas_price' - price of the gas;
"""
def getGasPrise(network): 
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(network)
		data = json.loads(response.text)
		gas_price = int(float(data['result']['FastGasPrice']) * 1e9)
		if (data['status'] == '1' and gas_price < gas_price * 5):  #  for Fantom network
			print('Normal price')
			return gas_price
		elif(data['status'] == '1' and gas_price > gas_price * 5):  #  for Fantom network
			print('Price * 5') 
			return gas_price * 5
		else: return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		return 0

""" Function parsing price of the cryptocurrency in USD from 'Cryptocompare'

'currency_eth' - array of crypto currencys(CC)
'data' - converting it to a dictionary;
'price' - turn the USD price into a number with a power of 6;
"""
def priceFromCryptocompare(currency):
	session = Session()
	session.headers.update(headers)  
	try:
		''' Ethereum network (USDC 6 decimals)'''
		if currency == 'CRV' or currency == 'crv':
			response = session.get('https://min-api.cryptocompare.com/data/price?fsym=CRV&tsyms=USD')
			data_eth = json.loads(response.text) 
			return int(data_eth['USD'] * pow(10, eth_decimals))
		if currency == 'WETH' or currency == 'weth':
			response = session.get('https://min-api.cryptocompare.com/data/price?fsym=WETH&tsyms=USD')
			data_eth = json.loads(response.text) 
			return int(data_eth['USD'] * pow(10, eth_decimals))
		if currency == 'FARM' or currency == 'farm':
			response = session.get('https://min-api.cryptocompare.com/data/price?fsym=FARM&tsyms=USD')
			data_eth = json.loads(response.text) 
			return int(data_eth['USD'] * pow(10, eth_decimals))
		else: 
			print('Only:\n"CRV" / "crv",\n"WETH" / "weth",\n"FARM" / "farm')
			return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(Cryptocompare)')
		return 0

""" Function parsing price of the cryptocurrency in USD from 'CoinGecko'

'currency_eth' - array of crypto currencys(CG);
'data' - converting it to a dictionary;
'usd_' - the price from JSON;
'price' - turn the USD price into a number with a power of 6;
"""
def priceFromCoinGecko(currency):
	session = Session()
	session.headers.update(headers) 
	try:
		''' Ethereum network (USDC 6 decimals)'''
		if currency == 'CRV' or currency == 'crv':
			response = session.get('https://api.coingecko.com/api/v3/coins/curve-dao-token')
			data_eth = json.loads(response.text)
			usd_ = data_eth['market_data']['current_price']['usd']
			return int(usd_ * pow(10, eth_decimals))
		if currency == 'WETH' or currency == 'weth':
			response = session.get('https://api.coingecko.com/api/v3/coins/weth')
			data_eth = json.loads(response.text)
			usd_ = data_eth['market_data']['current_price']['usd']
			return int(usd_ * pow(10, eth_decimals))
		if currency == 'FARM' or currency == 'farm':
			response = session.get('https://api.coingecko.com/api/v3/coins/harvest-finance')
			data_eth = json.loads(response.text)
			usd_ = data_eth['market_data']['current_price']['usd']
			return int(usd_ * pow(10, eth_decimals))
		else: 
			print('Only:\n"curve-dao-token",\n"weth",\n"harvest-finance" ')
			return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(CoinGecko)')
		return 0

""" A function for creating transactions 

'gasPrice/ETH/FTM..' - calling 'getGasPrise()' a function and getting a price on gas;
'nonce' - getting a nonce from the address;
"""
def test():
	nonce = w3.eth.get_transaction_count(address)
	gasPriceETH = 0
	gasPriceFTM = 0

	crv = w3.eth.contract(address=address_crv, abi=abi_crv)
	weth = w3.eth.contract(address=address_weth, abi=abi_weth)
	farm = w3.eth.contract(address=address_farm, abi=abi_farm)

	networks = data['networks']
	contracts_eth = [crv, weth, farm]
	tokens_eth = data['tokensETH']
	urls = data['url']

	for url in urls:
		for ur in url:
			if ur == 'ETH':
				gasPriceETH = getGasPrise(url[ur])
				print(gasPriceETH)
			if ur == 'FTM':
				gasPriceFTM = getGasPrise(url[ur])
				print(gasPriceFTM)

	for network in networks:
		for net in network:
				if net == 'ETH':
					for index, token in enumerate(tokens_eth):
						for ide in token:
							if ide == 'name':
								print(f'Network:{network[net]}, token:{token[ide]}, price:{priceFromCryptocompare(token[ide])}')	
								tx = contracts_eth[index].functions.setPriceInUSD(priceFromCryptocompare(token[ide])).build_transaction({
									'nonce': nonce,
									'chainId': 4,
									'gasPrice': gasPriceETH,
									'gas': 3000000,
								})
								nonce +=1
								signed_tx = w3.eth.account.sign_transaction(tx, private_key=SECRET)
								res =  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
								print(f'Network:{network[net]}:{w3.toHex(res)}')
				#if net == 'FTM':
						#print(network[net])

test()
