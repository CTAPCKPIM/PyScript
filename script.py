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

eth_decimals = 6

etherscan = 'https://api.etherscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken'

#print(w3.isConnected())
limit = 0
#print('Limit: ', limit)

def getGasLimit():
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(etherscan)  # for fantom
		data_ETH = json.loads(response.text)
		if (data_ETH['status'] == '1'):
			return int(float(data_ETH['result']['FastGasPrice']) * 1e9)  
		else: return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		return 0

limit = getGasLimit()
#print('New limit: ', limit)
#print('Type: ', type(limit))

""" Function parsing price of the gas

'data_ETH' - api.etherscan.com;
"""
def getGasPrise():
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(etherscan)
		data_ETH = json.loads(response.text)
		import pdb; pdb.set_trace()  #pdb.set_trace()
		gas_price = int(float(data_ETH['result']['FastGasPrice']) * 1e9)
		print('Gas price: ', gas_price) 
		print('Type: ', type(gas_price))
		if (data_ETH['status'] == '1' and gas_price < limit * 5):
			print('Normal price')
			return gas_price
		elif(data_ETH['status'] == '1' and gas_price > limit * 5):  #  for fantom
			print('Price * 5') 
			return gas_price * 5
		else: return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		return 0

getGasPrise()
#print(a)

""" Function parsing price of the cryptocurrency in USD from 'Cryptocompare'

'currency_eth' - array of crypto currencys(CC);
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
			#print(i)
			response = session.get('https://min-api.cryptocompare.com/data/price?fsym='+ i +'&tsyms=USD')
			data = json.loads(response.text) 
			#print(i, ': ', data['USD'])
			price = int(data['USD'] * pow(10, eth_decimals)) 
			print(price)
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
			#print(i)
			response = session.get('https://api.coingecko.com/api/v3/coins/' + i)
			data = json.loads(response.text)
			#print(i, ': ', data['market_data']['current_price']['usd'])
			usd_ = data['market_data']['current_price']['usd']
			price = int(usd_ * pow(10, eth_decimals)) 
			print(price)
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(CoinGecko)')
		return 0

#priceFromCoinGecko()

''' Other network '''

