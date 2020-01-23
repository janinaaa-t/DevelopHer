import time
from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.middleware import geth_poa_middleware

node_url = 'https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d'
contract_source_path = 'voting_contract.sol'
from_account_file = "account.silke.json"


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)


def deploy_contract(w3, contract_interface, private_key):
    contract = w3.eth.contract(abi=contract_interface['abi'],
                               bytecode=contract_interface['bin'])

    acct = w3.eth.account.privateKeyToAccount(private_key)
    construct_txn = contract.constructor().buildTransaction({
        'from':
        acct.address,
        'nonce':
        w3.eth.getTransactionCount(acct.address),
        'gas':
        4727597,
        'gasPrice':
        w3.toWei('21', 'gwei')
    })
    signed = acct.signTransaction(construct_txn)
    return w3.eth.sendRawTransaction(signed.rawTransaction).hex()


def wait_for_receipt(w3, tx_hash, poll_interval):
    while True:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        time.sleep(poll_interval)


if __name__ == '__main__':
    W3 = Web3(Web3.HTTPProvider(node_url))
    W3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with open(from_account_file) as keyfile:
        encrypted_key = keyfile.read()
        private_key = W3.eth.account.decrypt(encrypted_key, '')

    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()

    hash = deploy_contract(W3, contract_interface, private_key)
    receipt = W3.eth.waitForTransactionReceipt(hash)

    print('contractAddress: ' + receipt['contractAddress'] + '\n' +
          'transactionHash: ' + receipt['transactionHash'].hex() + '\n')
