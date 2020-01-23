from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

node_url = 'https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d'

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

###############################Customize these values###################
keyfile = 'account.silke.json'
password = ''
receiver_addresses = ['0x2418B7e00C5B8590d6FeB89f1e70f9A13A4181f7']
value = 0.01
########################################################################

transaction_template = {
    'to': None,
    'value': None,
    'gas': 2000000,
    'gasPrice': None,
    'nonce': None,
    'chainId': 4
}


def import_keyfile(keyfile: str):
    with open(keyfile, "r") as keyfile:
        account_json = keyfile.read()
        private_key = Account.decrypt(account_json, password)
    return Account.privateKeyToAccount(private_key)


def create_transaction(to: str, value: float, nonce):
    transaction = transaction_template.copy()

    transaction['to'] = to
    transaction['value'] = w3.toWei(value, 'ether')
    transaction['gasPrice'] = w3.toWei(25, 'gwei')
    transaction['nonce'] = nonce
    return transaction


def send_transaction(receiver: str, value: float, nonce):
    transaction = create_transaction(receiver, value, nonce)
    signed_transaction = from_account.sign_transaction(transaction)
    return w3.eth.sendRawTransaction(signed_transaction.rawTransaction)


if __name__ == '__main__':

    from_account = import_keyfile(keyfile)

    transaction_hashes = []
    print('sending transactions!')

    nonce = w3.eth.getTransactionCount(from_account.address)
    for receiver in receiver_addresses:
        transaction_hash = send_transaction(receiver, value, nonce)

        transaction_hashes.append(transaction_hash)
        print('successfully sent ' + str(transaction_hash.hex()))
        nonce = nonce + 1

    for hash in transaction_hashes:
        transaction_receipt = w3.eth.waitForTransactionReceipt(hash)
        print("transaction successfully mined: " + str(hash.hex()))
