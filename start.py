import sys
sys.path.insert(0, '../abcFinance')
import abce
from bank import Bank
from household import Household

min_capital_ratio = 0

sim = abce.Simulation()
bank = sim.build_agents(Bank, 'bank', number=1, min_capital_ratio=min_capital_ratio, reserves=100, deposits=100)
households = sim.build_agents(Household, 'household', number=100, money=100, loans=0)

households.request_loans()
bank.grant_loans()
print('bank')
bank.print_balance_sheet()

households.pay_interest()

bank.print_profit_and_loss()
bank.book_end_of_period()
households.book_end_of_period()
bank.print_balance_sheet()

households.repay_loan_principal()
print('bank')
bank.print_balance_sheet()
print('household 0')
households[0].print_balance_sheet()
