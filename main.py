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
load_dotenv()

with open('dataset3.json') as f:
    data = json.load(f)

# 'headers' - requesting JSON from the site;
headers = { 
	'Accepts': 'application/json'
}

""" All variables

Dotenv variables:
 'API' - loading the variable;
 'INFURA' - your address of the provider; 
 'SECRET' - your private key;

Other variables:
 'cc' - connecting Сryptocompare;
 'cg' - connecting CoinGecko;
 'w3' - connecting Web3;
 'eth_decimals' - decimals of USDC in ETH network;
"""
API = os.getenv('API_KEY')
INFURA = os.getenv('INFURA_URL')
SECRET = os.getenv('SECRET_KEY')

# Connecting providers
cc = cc.cryptocompare._set_api_key_parameter(API)
cg = CoinGeckoAPI()
w3 = Web3(Web3.HTTPProvider(INFURA))
w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

# Variables for decimals 
eth_decimals = 6
address = '0xf39D262c556aBefFC619847eE0355af42c4d0e91'

""" Function parsing price of the gas

 'data' - JSON from scans; 
 'gas_price' - price of the gas;
"""
def getGasPrice(network): 
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(network)
		data = json.loads(response.text)
		gas_price = int(float(data['result']['FastGasPrice']) * 1e9)
		if (data['status'] == '1' and gas_price < gas_price * 5):
			print('Price: Normal')
			return gas_price
		elif(data['status'] == '1' and gas_price > gas_price * 5):
			print('Price: Overpriced') 
			return gas_price * 5
		else: return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		return 0

""" Function parsing price of the cryptocurrency in USD from 'Cryptocompare'

 'data_eth' - converting it to a dictionary;
  Return the USD price into a number with a power of 6;
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
			return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(Cryptocompare)')
		return 0

""" Function parsing price of the cryptocurrency in USD from 'CoinGecko'

 'data_eth' - converting it to a dictionary;
 'usd_' - the price from JSON;
  Return the USD price into a number with a power of 6;
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
			return 0
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(CoinGecko)')
		return 0

""" A function for creating transactions 

'contract' - initializing an object 'contract';
'price' - returning a price;
'chainId' - returning an id of chain;
'gasPrice' - returning a gas price;
'nonce' - getting a nonce from the address;
"""
def testNEW():
	nonce = w3.eth.get_transaction_count(address)
	for key in data:
		tokens = key.get('tokens')
		for token in tokens:
			#import pdb;pdb.set_trace()
			abi_ = token.get('abi')
			address_ = token.get('address')
			contract = w3.eth.contract(address=address_, abi=abi_)
			price = priceFromCryptocompare(token.get('name'))
			chainId = key.get('id') 
			gasPrice = getGasPrice(key.get('url'))
			tx = contract.functions.setPriceInUSD(price
				).build_transaction(
				{
					'nonce':nonce,
					'chainId':chainId,
					'gasPrice':gasPrice,
					'gas':1000000,
				})
			nonce +=1
			signed_tx = w3.eth.account.sign_transaction(tx, private_key=SECRET)
			res = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
			print(f"Token: {token.get('name')} => {w3.toHex(res)}")

testNEW()