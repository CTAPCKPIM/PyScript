# -*- coding: utf-8 -*-

import requests
import json
import os
import cryptocompare as cc

from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


# load the configuration from a .env
load_dotenv()

# loading the variable
API = os.getenv('API_KEY')

# requesting JSON from the site
headers = { 
	'Accepts': 'application/json'
}

ccobj = cc.cryptocompare._set_api_key_parameter(API)
cg = CoinGeckoAPI()

''' Ethereum network '''
def PriceFromCryptocompare():
	session = Session()
	session.headers.update(headers)
	currency = ['CRV', 'WETH', 'FARM'] #array of crypto currencys(CC)
	try:
		for i in currency:
			#print(i)
			response = session.get('https://min-api.cryptocompare.com/data/price?fsym='+ i +'&tsyms=USD')
			data = json.loads(response.text) #converting it to a dictionary
			print(i, ': ', data['USD'])
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(Cryptocompare)')
		return 0

PriceFromCryptocompare()

def PriceFromCoinGecko():
	session = Session()
	session.headers.update(headers)
	currency = ['curve-dao-token', 'weth', 'harvest-finance'] #array of crypto currencys(CG)
	try:
		for i in currency:
			#print(i)
			response = session.get('https://api.coingecko.com/api/v3/coins/' + i)
			data = json.loads(response.text)
			print(i, ': ', data['market_data']['current_price']['usd'])
	except (ConnectionError, Timeout, TooManyRedirects, KeyError):
		print('Error: connecting not successful(CoinGecko)')
		return 0

PriceFromCoinGecko()

''' Other network '''


'''
#print('\nCryptocompare:')
#print('|',cc.get_price('CRV', currency='USD'))
#print('|',cc.get_price('WETH', currency='USD'))
#print('|',cc.get_price('FARM', currency='USD'))

#print('\nCoinGecko:')
#print('|',cg.get_price(ids='curve-dao-token', vs_currencies='usd'))
#print('|',cg.get_price(ids='weth', vs_currencies='usd'))
#print('|',cg.get_price(ids='harvest-finance', vs_currencies='usd'))

while True:
	print(cc.get_price('BNB', currency='USD'))

for i in cc.get_coin_list(format=False):
	print(i)
'''	