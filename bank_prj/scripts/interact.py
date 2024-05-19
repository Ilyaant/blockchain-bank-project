import os
from brownie import Contract, accounts, network
from dotenv import load_dotenv
load_dotenv()
network.connect('ganache-local')

account = accounts.add(os.getenv('PRIVATE_KEY'))
account1 = accounts.add(os.getenv('PRIVATE_KEY1'))
account2 = accounts.add(os.getenv('PRIVATE_KEY2'))
account3 = accounts.add(os.getenv('PRIVATE_KEY3'))
credit_contract = Contract('0x38308EC3a90E733A8478D587dd806809cbaAd888')
bank_contract = Contract('0x9A6e4616C190b98AB1A6EFfafEb05BdCBd7e8216')

curr_balance = bank_contract.getStorage({'from': account})
print(f'Current balance: {curr_balance}')

bank_contract.register('acc0', 'acc0', 2000, {'from': account})
bank_contract.register('acc1', 'acc1', 1000, {'from': account1})
bank_contract.register('acc2', 'acc2', 2000, {'from': account2})
bank_contract.register('acc3', 'acc3', 0, {'from': account3})