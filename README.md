**Table of Contents**

- [DevelopHer](#developher)
    - [Setup](#setup)
    - [Create Account](#create-account)
    - [Share Ether](#share-ether)
    - [Send A Transaction](#send-a-transaction)
    - [Deploy The Smart Contract](#deploy-the-smart-contract)
    - [Vote](#vote)
    - [Winning proposal](#winning-proposal)
    - [Utilities](#utilities)
        - [Account-Address](#account-address)
        - [Print Blocks](#print-blocks)

# DevelopHer
This is a small tutorial to create an account, setup a smart contract and send transactions to it.

## Setup
I included the `.venv/` directory, so all dependencies should be in place. Especially the Solidity-Compiler solc is included, which is needed for the library py-solc, which we are using.
To activate the virtual environment from the command-line, execute `$ source .venv/bin/activate` from the project root directory.
It should not be necessary to do anything if you are using PyCharm.

## Create Account
To create an account, execute [create_account.py](create_account.py). A file called `account.json` should be created, which contains your account.

## Share Ether
To share ether with other addresses, fill in the addresses and the amount of ether to be shared in the [share_ether.py](share_ether.py).

## Send A Transaction
If you want to send ether to another address, use [make_transaction.py](make_transaction.py). This is basically the same as in [share_ether.py](share_ether.py).
Don't forget to customize the receiver and the value that is being sent.

## Deploy The Smart Contract
To deploy the smart contract use [deploy_contract.py](deploy_contract.py). The contract that is being deployed is stored in [voting_contract.sol](voting_contract.sol).
It is an adaptation of the smart contract given in the solidity-documentation, and lets participants vote for one of the proposals.
Make sure to customize the `proposals` and the `voters` fields.

After you deployed the contract, make sure to note the smart contract address, you will need it, if you want to vote! It is printed in the console.

## Vote
To vote, open the file [vote.py](vote.py), edit the contract address and the proposal-number.

## Winning proposal
To get the winning proposal, visit [get_winning_proposal.py](get_winning_proposal.py). Don't forget to edit the contract-address!

## Utilities

### Account-Address
If you forgot to note your account-address down, don't despair, just use [this](get_account_address.py) little script!

### Print Blocks
If you are interested in the currently mined blocks and their meta-data use [this](print_block.py) script.
