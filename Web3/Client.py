from web3 import Web3
from FSON import DICT
# from web3.auto import w3

infura_provider = "https://mainnet.infura.io/v3/ae463de8b055408e91bc6dee9b53a96c"
# w3 = Web3(EthereumTesterProvider())
w3 = Web3(Web3.HTTPProvider(infura_provider))
print(w3.isConnected())
item = w3.eth.get_block('latest')

print(DICT.to_pretty_json(item.__dict__))
