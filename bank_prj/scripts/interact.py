import os
from brownie import Contract, accounts, network
from dotenv import load_dotenv
load_dotenv()
network.connect('ganache-local')

account = accounts.add(os.getenv('PRIVATE_KEY'))
account1 = accounts.add(os.getenv('PRIVATE_KEY1'))
account2 = accounts.add(os.getenv('PRIVATE_KEY2'))
credit_contract = Contract('0x5b0630DDF920A7a91A6eD8B96fdfB22589783e14')
bank_contract = Contract('0xB6DEBA730C1Dd36E11cd7dB243f1727533828D0e')

curr_balance = bank_contract.getStorage({'from': account})
print(f'Current balance: {curr_balance}')