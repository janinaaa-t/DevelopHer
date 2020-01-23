from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source

node_url = 'https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d'
contract_source_path = 'voting_contract.sol'
from_account_file = "account.json"

proposal = "Pizza"


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)


def vote(W3, contract_interface, private_key, proposal):
    contract = W3.eth.contract(abi=contract_interface['abi'],
                               bytecode=contract_interface['bin'])

    acct = W3.eth.account.privateKeyToAccount(private_key)

    construct_txn = contract.giveRightToVote(proposal).buildTransaction({
        'from':
            acct.address,
        'nonce':
            W3.eth.getTransactionCount(acct.address),
        'gas':
            4727597,
        'gasPrice':
            W3.toWei('21', 'gwei')
    })

    signed = acct.signTransaction(construct_txn)
    transaction_hash = W3.eth.sendRawTransaction(signed.rawTransaction).hex()
    W3.eth.waitForTransactionReceipt(transaction_hash)
    print("Vote completed")


if __name__ == '__main__':
    W3 = Web3(Web3.HTTPProvider(node_url))
    W3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with open(from_account_file) as keyfile:
        encrypted_key = keyfile.read()
        private_key = W3.eth.account.decrypt(encrypted_key, '')

    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    vote(W3, contract_interface, private_key, proposal)
