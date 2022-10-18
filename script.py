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

with open('dataset.json') as f:
    data = json.load(f)

with open('APIs.json') as f_:
    APIs = json.load(f_)

# 'headers' - requesting JSON from the site;
headers = { 
	'Accepts': 'application/json'
}

""" All variables

Dotenv variables:
 'API' - loading the variable; 
 'SECRET' - your private key;

Other variables:
 'cc' - connecting Сryptocompare;
 'cg' - connecting CoinGecko;
 'usdc_decimals' - decimals of USDC in networks;
"""
API = os.getenv('API_KEY')
SECRET = os.getenv('SECRET_KEY')

# Connecting providers
cc = cc.cryptocompare._set_api_key_parameter(API)
cg = CoinGeckoAPI()

# Variables for decimals 
usdc_decimals = 6
address = '0xf39D262c556aBefFC619847eE0355af42c4d0e91'

""" Function parsing price of the gas

 'data' - JSON from scans; 
 'gas_price' - price of the gas;
"""
def getGasPrice(network, chainId): 
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(network)
		data = json.loads(response.text)
		if(chainId == 5 and data['status'] == '1'):
			gas_price = int(float(data['result']['FastGasPrice']) * 1e9)
			if(gas_price < gas_price * 5):
				print('Price(gas): Normal')
				return gas_price
			else:
				print('Price(gas): Overpriced')  
				return gas_price * 5
		if(chainId == 4002 and data['status'] == '1'):
			gas_price = int(float(data['result']['FastGasPrice']) * 1e9)
			if(gas_price < gas_price * 5):
				print('Price(gas): Normal')
				return gas_price
			else:
				print('Price(gas): Overpriced')  
				return gas_price * 5
		if(chainId == 80001 and data['status'] == '1'):
			gas_price = int(float(data['result']['FastGasPrice']) * 1e9)
			if(gas_price < gas_price * 5):
				print('Price(gas): Normal')
				return gas_price
			else: 
				print('Price(gas): Overpriced') 
				return gas_price * 5
		if(chainId == 97 and data['status'] == '1'):
			gas_price = int(float(data['result']['FastGasPrice']) * 1e9)
			if(gas_price < gas_price * 5):
				print('Price(gas): Normal')
				return gas_price
			else: 
				print('Price(gas): Overpriced') 
				return gas_price * 5
		if(chainId == 43113): 
			print('Price(gas): Normal')
			return int(data['result'], 16)
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
		response = session.get('https://min-api.cryptocompare.com/data/price?fsym='+ currency +'&tsyms=USD')
		data_eth = json.loads(response.text) 
		return int(data_eth['USD'] * pow(10, usdc_decimals))
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
		response = session.get('https://api.coingecko.com/api/v3/coins/' + currency)
		data_eth = json.loads(response.text)
		usd_ = data_eth['market_data']['current_price']['usd']
		return int(usd_ * pow(10, usdc_decimals))
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(CoinGecko)')
		return 0

""" A function for creating transactions(Cryptocompare)

'count' - number of the smart contract;
'tokens' - array with tokens information;
'api' - APIs of providers;
'provider' - addresses of providers;
'full' - full address after concatenation 'provider' + 'api';
'w3' - connecting Web3;
'nonce' - getting a nonce from the address;
'abi_' - ABI of contracts;
'address_' - address of contracts;
'contract' - initializing an object 'contract';
'price' - returning a price;
'chainId' - returning an id of chain;
'rpc' - address of the gas price;
'gasPrice' - returning a gas price;
"""
def cryptocompareTransactions():
	print('Cryptocompare:')
	count = 0
	for key in data:
		tokens = key.get('tokens')
		api = APIs[str(key.get('id'))]
		provider = key.get('provider')
		full = provider + api
		w3 = Web3(Web3.HTTPProvider(full))
		nonce = w3.eth.get_transaction_count(address)
		w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
		for token in tokens:
			abi_ = token.get('abi')
			address_ = token.get('address')
			contract = w3.eth.contract(address=address_, abi=abi_)
			price = priceFromCryptocompare(token.get('name'))
			chainId = key.get('id')
			rpc = key.get('url') 
			gasPrice = getGasPrice(rpc, chainId)
			tx = contract.functions.setPriceInUSD(price
				).build_transaction(
				{
					'nonce':nonce,
					'chainId':chainId,
					'gasPrice':gasPrice,
					'gas':450000,
				})
			nonce +=1
			count +=1
			signed_tx = w3.eth.account.sign_transaction(tx, private_key=SECRET)
			res = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
			print(f"Contract№: {count}\nToken: {token.get('name')} => {w3.toHex(res)}\nPrice(USDC): {price}\n===\n")

""" A function for creating transactions(CoinGecko)

'count' - number of the smart contract;
'tokens' - array with tokens information;
'api' - APIs of providers;
'provider' - addresses of providers;
'full' - full address after concatenation 'provider' + 'api';
'w3' - connecting Web3;
'nonce' - getting a nonce from the address;
'abi_' - ABI of contracts;
'address_' - address of contracts;
'contract' - initializing an object 'contract';
'price' - returning a price;
'chainId' - returning an id of chain;
'rpc' - address of the gas price;
'gasPrice' - returning a gas price;
"""
def coinGeckoTransactions():
	print('CoinGecko:')
	count = 0
	for key in data:
		tokens = key.get('tokens')
		api = APIs[str(key.get('id'))]
		provider = key.get('provider')
		full = provider + api
		w3 = Web3(Web3.HTTPProvider(full))
		nonce = w3.eth.get_transaction_count(address)
		w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
		for token in tokens:
			abi_ = token.get('abi')
			address_ = token.get('address')
			contract = w3.eth.contract(address=address_, abi=abi_)
			price = priceFromCoinGecko(token.get('longName'))
			chainId = key.get('id')
			rpc = key.get('url') 
			gasPrice = getGasPrice(rpc, chainId)
			tx = contract.functions.setPriceInUSD(price
				).build_transaction(
				{
					'nonce':nonce,
					'chainId':chainId,
					'gasPrice':gasPrice,
					'gas':450000,
				})
			nonce +=1
			count +=1
			signed_tx = w3.eth.account.sign_transaction(tx, private_key=SECRET)
			res = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
			print(f"Contract№: {count}\nToken: {token.get('name')} => {w3.toHex(res)}\nPrice(USDC): {price}\n===\n")

""" The primary function of a choice provider of prices

 Using 'Cryptocompare', and CoinGecko services.
"""
def main():
	try:
		# If errors do not exist used 'cryptocompareTransactions()'
		cryptocompareTransactions()
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		# else used 'coinGeckoTransactions()'
		coinGeckoTransactions()
main()