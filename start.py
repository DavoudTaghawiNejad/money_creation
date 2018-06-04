import abce as abcEconomics
from bank import Bank
from household import Household

min_capital_ratio = 0.03

sim = abcEconomics.Simulation()
bank = sim.build_agents(Bank, 'bank', number=1, min_capital_ratio=min_capital_ratio, reserves=11000, deposits=10000)
households = sim.build_agents(Household, 'household', number=100, money=100, loans=0)


for time in range(100):
    sim.advance_round(time)
    ir = bank.announce_interest_rate()
    households.request_loans(list(ir)[0])
    bank.grant_loans()
    print('bank')
    bank.print_balance_sheet()

    households.pay_interest()

    bank.print_profit_and_loss()
    bank.book_end_of_period()
    households.book_end_of_period()
    bank.print_balance_sheet()

    print('bank')
    bank.print_balance_sheet()
    print('household 0')
    households[0].print_balance_sheet()
    print('household 1')
    households[1].print_balance_sheet()
    households.return_money()
    households.repay_loan_principal()
    bank.pay_dividents()
sim.graph()
