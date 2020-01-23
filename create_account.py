import json
from os import path

from eth_account import Account

if __name__ == '__main__':
    account = Account.create()
    print("this is my account:")
    print("adress: " + str(account.address))
    print("private: " + str(account.privateKey.hex()))

    encrypted_account = account.encrypt("")

    with open("account.json", "w") as file:
    if path.exists:
        print('Keyfile ' + keyfile + " already exists")
        exit(1)
        file.write(json.dumps(encrypted_account))
