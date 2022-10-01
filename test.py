import json

with open('dataset.json') as f:
    data = json.load(f)

networks = data['networks']
tokens_eth = data['tokensETH']
tokens_ftm = data['tokensFTM']

""" Функция для прикрепления СЕТЬ > ТОКЕН """
def setTokenOfNetwork():
    for net in networks:
        for index in net:
            if index == 'ETH':
                for token in tokens_eth:
                    for ide in token:
                        if ide == 'name':     
                            print(f'Network: {net[index]} = token: {token[ide]}')
            if index == 'FTM':
                for token in tokens_ftm:
                    for idf in token:
                        if idf == 'name':
                            print(f'Network: {net[index]} = token: {token[idf]}')
                        

#setTokenOfNetwork()

print("=" * 50)

def setLongName():
    for net in networks:
        for index in net:
            if index == 'ETH':
                for token in tokens_eth:
                    for ide in token:
                        if ide == 'longName':
                            print(f'Network: {net[index]},token: {token[ide]}')
            if index == 'FTM':
                for token in tokens_ftm:
                    for idf in token:
                        if idf == 'longName':
                            print(f'Network: {net[index]},token: {token[idf]}')

#setLongName()


'''for section, commands in data.items():
    #print(section)
    #print('\n'.join(map(str, commands)))
    print(section, commands, '\n')
'''
'''
network = ['ETH', 'FTM', 'Polygon', 'BSC', 'AVAX']

contracts_eth = ['crv', 'weth', 'farm']
contracts_ftm = ['spirit', 'wftm', 'yfi']
contracts_pol = ['quick', 'orbs', 'wmatic']
contracts_bsc = ['wbnb', 'cake', 'stg']
contracts_avax = ['wavax', 'spell', 'ptp']

tokens_eth = ['crv', 'weth', 'farm']
tokens_ftm = ['spirit', 'wftm', 'yfi']
tokens_pol = ['quick', 'orbs', 'wmatic']
tokens_bsc = ['wbnb', 'cake', 'stg']
tokens_avax = ['wavax', 'spell', 'ptp']

for n in network:
    if n == network[0]:
        for ide, contract in enumerate(contracts_eth):
            print(f'network: {n}, contract: {contract}, token: {tokens_eth[ide]}')
    if n == network[1]:
        for idf, contract in enumerate(contracts_ftm):
            print(f'network: {n}, contract: {contract}, token: {tokens_ftm[idf]}')
    if n == network[2]:
        for idp, contract in enumerate(contracts_pol):
            print(f'network: {n}, contract: {contract}, token: {tokens_pol[idp]}')
    if n == network[3]:
        for idb, contract in enumerate(contracts_bsc):
            print(f'network: {n}, contract: {contract}, token: {tokens_bsc[idb]}')
    if n == network[4]:
        for ida, contract in enumerate(contracts_avax):
            print(f'network: {n}, contract: {contract}, token: {tokens_avax[ida]}')
'''