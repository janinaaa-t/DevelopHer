import json

from eth_account import Account

if __name__ == '__main__':
    account = Account.create()
    print("this is my account:")
    print("adress: " + str(account.address))
    print("private: " + str(account.privateKey.hex()))

    encrypted_account = account.encrypt("")

    with open("account.json", "w") as file:
        file.write(json.dumps(encrypted_account))
