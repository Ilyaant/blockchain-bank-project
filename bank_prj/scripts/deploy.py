import os
from brownie import accounts, CreditToken, Bank
from dotenv import load_dotenv
load_dotenv()

def main():
    account = accounts.add(os.getenv('PRIVATE_KEY'))
    credit_address = CreditToken.deploy(account, {'from': account})

    Bank.deploy(credit_address, 200, {'from': account})