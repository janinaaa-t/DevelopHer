from eth_account import Account

keyfile = "account.json"


def import_key_file(keyfile: str):
    with open(keyfile, "r") as account_file:
        from_account_json = account_file.read()
    private_key = Account.decrypt(from_account_json, "")
    return Account.privateKeyToAccount(private_key)


if __name__ == '__main__':
    account = import_key_file(keyfile)
    print("account-adress: " + account.address)
