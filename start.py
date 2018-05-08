import sys
sys.path.insert(0, '../abcFinance')
import abce
from bank import Bank
from household import Household


sim = abce.Simulation()
bank = sim.build_agents(Bank, 'bank', number=1, reserves=100, deposits=100)
household = sim.build_agents(Household, 'household', number=1, money=100, loans=0)
bank_owner = sim.build_agents(Household, 'bank_owner', number=1, participations=100)


bank.book(debit=[('loans', 100)], credit=[('deposits', 100)], text='Loan granting')
household.book(debit=[('money', 100)], credit=[('loans', 100)], text='Take out loan')
print('Bank')
bank.print_balance_sheet()
print('Household')
household.print_balance_sheet()


household.book(debit=[('interest expenses', 10)], credit=[('money', 10)], text='Interest payment')
bank.book(debit=[('deposits', 10)], credit=[('interest income', 10)], text='Interest payment')
print('Bank')
bank.print_balance_sheet()
bank.print_profit_and_loss()
print('Household')
household.print_balance_sheet()
household.print_profit_and_loss()


bank.book(debit=[('equity', 10)], credit=[('deposits', 10)], text='Dividend payment')
bank_owner.book(debit=[('money', 10)], credit=[('dividend income', 10)], text='Dividend payment')
print('Bank')
bank.print_balance_sheet()
bank.print_profit_and_loss()
print('Bank owner')
bank_owner.print_balance_sheet()
bank_owner.print_profit_and_loss()


household.book(debit=[('loans', 100)], credit=[('money', 100)], text='Principal repayment')
bank.book(debit=[('deposits', 100)], credit=[('loans', 100)], text='Principal repayment')
print('Bank')
bank.print_balance_sheet()
print('Household')
household.print_balance_sheet()
print('Bank owner')
bank_owner.print_balance_sheet()
