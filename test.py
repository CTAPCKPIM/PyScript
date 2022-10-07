import json
from datetime import datetime

timestamp = datetime.now()

with open('dataset2.json') as f:
    data = json.load(f)

contracts_eth = ['crv', 'weth', 'farm']
contracts_ftm = ['spirit', 'wftm', 'yfi']

def test():             
    for index in data:
        tokens = index.get('tokens')
        for num, token in enumerate(tokens):
                print(f"Network: {index.get('net')} => Token: {token.get('name')} => Contact: {contracts_eth[num]}")
                                     
test()
print(f'Time: {datetime.now() - timestamp}')
























def functionNEW(): 
    for network in networks:
        for net, url in network.items():
            if net == 'ETH':
                for token in tokens_eth:
                    for name, symbols in token.items():
                        if name == 'name':
                            print(f'| Network: {net} => token: {symbols} ')                                            
            if net == 'FTM':
                for token in tokens_ftm:
                    for name, symbols in token.items():
                        if name == 'name':
                            print(f'| Network: {net} => token: {symbols} ')
                        
#functionNEW()
#print(f'Time: {datetime.now() - timestamp}')

'''
network = ['ETH', 'FTM', 'Polygon', 'BSC', 'AVAX']
'''