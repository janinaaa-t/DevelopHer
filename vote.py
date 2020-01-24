import json

from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source

##############################Customize these filds##########################
contract_address = '0xff722329d2B5f708408bf7619C5C11D6e8F64698'
proposal = 1  # Number of the proposal ( Counting starts of course with 0 ;-))
from_account_file = 'account.silke.json'
password = ''
#############################################################################

node_url = 'https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d'


def vote(W3, private_key, proposal):

    with open('abi.json', 'r') as abi_file:
        abi = json.load(abi_file)

    contract = W3.eth.contract(abi=abi,
                               address=contract_address)

    acct = W3.eth.account.privateKeyToAccount(private_key)

    construct_txn = contract.functions.vote(proposal).buildTransaction({
        'from':
            acct.address,
        'nonce':
            W3.eth.getTransactionCount(acct.address),
        'gas':
            4727597,
        'gasPrice':
            W3.toWei('21', 'gwei'),
        'chainId': 4
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
        private_key = W3.eth.account.decrypt(encrypted_key, password)

    vote(W3, private_key, proposal)
