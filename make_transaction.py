from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

########################Customize these fields###########################
keyfile = 'account.json'
password = ''
to_adress = '0x2418B7e00C5B8590d6FeB89f1e70f9A13A4181f7'
value = '0.01'  # value in Ether
#########################################################################

node_url = "https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d"

transaction_template = {
    'to': None,
    'value': None,
    'gas': 2000000,
    'gasPrice': None,
    'nonce': None,
    'chainId': 4
}


def import_keyfile(keyfile: str):
    with open(keyfile, "r") as account_file:
        from_account_json = account_file.read()
    private_key = Account.decrypt(from_account_json, password)
    return Account.privateKeyToAccount(private_key)


def create_transaction(from_account, to, value):
    transaction = transaction_template.copy()

    transaction['to'] = to
    transaction['value'] = w3.toWei(value, 'ether')
    transaction['gasPrice'] = w3.toWei(25, 'gwei')
    transaction['nonce'] = w3.eth.getTransactionCount(from_account.address)
    return transaction


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider(node_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    from_account = import_keyfile(keyfile)

    new_transaction = create_transaction(from_account, to_adress, value)

    # signing transaction
    signed_Transaction = from_account.sign_transaction(new_transaction)

    # sending transaction
    transaction_hash = w3.eth.sendRawTransaction(signed_Transaction.rawTransaction)

    print("transaction hash: " +
          str(transaction_hash.hex()))

    # waiting for confirmation
    transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
    print(transaction_receipt)
