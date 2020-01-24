import json

from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source

#############################Customize this field###########################
contract_address = '0xff722329d2B5f708408bf7619C5C11D6e8F64698'
#########################################################################

node_url = 'https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d'
contract_source_path = 'voting_contract.sol'



if __name__ == '__main__':
    W3 = Web3(Web3.HTTPProvider(node_url))
    W3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with open('abi.json', 'r') as abi_file:
        abi = json.load(abi_file)

    contract = W3.eth.contract(abi=abi,
                               address=contract_address)

    winner_in_bytes = contract.functions.winnerName().call()
    and_the_winner_is = Web3.toText(winner_in_bytes)
    print("and the winner is: " + and_the_winner_is)
