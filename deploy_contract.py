import time
from web3 import Web3
from solc import compile_source
from web3.middleware import geth_poa_middleware

###############################Customize these fields######################
proposals = [
    str.encode('Pizza'),
    str.encode('Käsespätzle'),
    str.encode('Pfannkuchen')
]
voters = ["0x2418B7e00C5B8590d6FeB89f1e70f9A13A4181f7", "..."]

from_account_file = "account.silke.json"
password = ''
#############################################################################

contract_source_path = 'voting_contract.sol'

node_url = 'https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d'

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)


def deploy_contract(w3, contract_interface, account, nonce):
    contract = w3.eth.contract(abi=contract_interface['abi'],
                               bytecode=contract_interface['bin'])

    construct_txn = contract.constructor(proposals).buildTransaction({
        'from':
            account.address,
        'nonce':
            nonce,
        'gas':
            4727597,
        'gasPrice':
            w3.toWei('21', 'gwei')
    })
    signed = account.signTransaction(construct_txn)
    return w3.eth.sendRawTransaction(signed.rawTransaction).hex()


def wait_for_receipt(w3, tx_hash, poll_interval):
    while True:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        time.sleep(poll_interval)


def give_right_to_vote(contract, account, voters, nonce):
    transactions = []
    # create + send Transactions
    for voter in voters:
        construct_txn = contract.functions.giveRightToVote(
            voter).buildTransaction({
            'from':
                account.address,
            'nonce':
                nonce,
            'gas':
                4727597,
            'gasPrice':
                w3.toWei('21', 'gwei')
        })
        nonce = nonce + 1
        signed = account.signTransaction(construct_txn)
        transactions.append(
            w3.eth.sendRawTransaction(signed.rawTransaction).hex())

    # wait for receipts
    allowed_voters = 0
    for tx_hash in transactions:
        w3.eth.waitForTransactionReceipt(tx_hash)
        allowed_voters = allowed_voters + 1
        print("There are " + str(allowed_voters) + " allowed voters!")


if __name__ == '__main__':
    with open(from_account_file) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, password)

    acct = w3.eth.account.privateKeyToAccount(private_key)

    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()

    nonce = w3.eth.getTransactionCount(acct.address)

    transaction_hash = deploy_contract(w3, contract_interface, acct, nonce)
    nonce = nonce + 1

    receipt = w3.eth.waitForTransactionReceipt(transaction_hash)

    smart_contract_adress = receipt['contractAddress']

    print('contractAddress: ' + receipt['contractAddress'] + '\n' +
          'transactionHash: ' + receipt['transactionHash'].hex() + '\n')

    contract = w3.eth.contract(abi=contract_interface['abi'],
                               bytecode=contract_interface['bin'],
                               address=smart_contract_adress)
    give_right_to_vote(contract, acct, voters, nonce)
