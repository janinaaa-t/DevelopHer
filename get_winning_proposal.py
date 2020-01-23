import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source

node_url = 'https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d'
contract_source_path = 'voting_contract.sol'

contract_address = '0xff722329d2B5f708408bf7619C5C11D6e8F64698'


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)


if __name__ == '__main__':
    W3 = Web3(Web3.HTTPProvider(node_url))
    W3.middleware_onion.inject(geth_poa_middleware, layer=0)

    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()
    contract = W3.eth.contract(abi=contract_interface['abi'],
                               address=contract_address)

    winner_in_bytes = contract.functions.winnerName().call()
    and_the_winner_is = Web3.toText(winner_in_bytes)
    print("and the winner is: " + and_the_winner_is)
