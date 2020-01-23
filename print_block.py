import time

from web3 import Web3
from web3.middleware import geth_poa_middleware

node_url = "https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d"


def print_block(block):
    transactions = block.transactions
    print("\n\n\n")
    print("transactions of Block " + str(block.number))
    for transaction in transactions:
        print(transaction.hex())


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider(node_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    block_number = 0
    while True:
        latest_block = w3.eth.getBlock('latest')
        if latest_block.number != block_number:
            block_number = latest_block.number
            print_block(latest_block)
        time.sleep(3)
