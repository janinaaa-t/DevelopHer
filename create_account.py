import json
from os import path

from eth_account import Account

keyfile = 'account.json'
password = ''

if __name__ == '__main__':
    account = Account.create()
    print("this is my account:")
    print("adress: " + str(account.address))
    print("private: " + str(account.privateKey.hex()))

    encrypted_account = account.encrypt(password)
    if path.exists:
        print('Keyfile ' + keyfile + " already exists")
        exit(1)
    with open(keyfile, "w") as file:
        file.write(json.dumps(encrypted_account))
