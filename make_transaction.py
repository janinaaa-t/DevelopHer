from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

node_url = "https://rinkeby.infura.io/v3/646f232797a44ce58c336cf4e852905d"
from_account_file = "account.silke.json"
to_adress = '0x2418B7e00C5B8590d6FeB89f1e70f9A13A4181f7'

# Value in ether
value = '0.9'

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
    private_key = Account.decrypt(from_account_json, "")
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

    from_account = import_keyfile(from_account_file)

    new_transaction = create_transaction(from_account, to_adress, value)

    # Transaction signieren
    signed_Transaction = from_account.sign_transaction(new_transaction)

    # Transaction abschicken
    transaction_hash = w3.eth.sendRawTransaction(signed_Transaction.rawTransaction)

    print("transaction hash: " +
          str(transaction_hash.hex()))
    # auf Bestätigung warten
    transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
    print(transaction_receipt)
