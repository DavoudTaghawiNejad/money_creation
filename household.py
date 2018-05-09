import abcFinance
from random import normalvariate
from accountingsystem import s


class Household(abcFinance.Agent):
    def init(self, money=0, loans=0, participations=0):
        self.make_asset_accounts(['money', 'participations'])
        self.make_liability_accounts(['loans'])
        self.make_flow_accounts(['dividend income', 'interest expenses'])
        # self.make_residual_account('equity')
        self.book(debit=[('money', money), ('participations', participations)],
                  credit=[('loans', loans), ('equity', money + participations - loans)],
                  text='Initial endowment')
        self.book_end_of_period()
        self.bank = ('bank', 0)

    def request_loans(self, interest_rate):
        self.interest_rate = interest_rate
        money = self.accounts['money'].get_balance()[1]
        if (self.accounts['money'].get_balance()[0] != s.CREDIT and
                money >= self.interest_rate):
            amount = truncnorm(0, money // self.interest_rate, sigma=100)
            self.send(self.bank, 'request_loan', amount)

    def pay_interest(self):
        _, loan = self.accounts['loans'].get_balance()
        interest_payment = loan * self.interest_rate
        self.make_interest_payment(interest_payment, self.bank)

    def repay_loan_principal(self):
        _, loan = self.accounts['loans'].get_balance()
        self.repay_loan(loan, self.bank)

    def return_money(self):
        _, money = self.accounts['money'].get_balance()
        self.log('money', money)








    # hide

    def make_interest_payment(self, interest_payment, bank):
        self.book(debit=[('interest expenses', interest_payment)],
                  credit=[('money', interest_payment)],
                  text='Interest payment')

        self.send(bank, '_autobook', dict(
            debit=[('deposits', interest_payment)],
            credit=[('interest income', interest_payment)],
            text='Interest payment'))

    def repay_loan(self, loan, bank):
        self.book(debit=[('loans', loan)],
                  credit=[('money', loan)],
                  text='Principal repayment')

        self.send(bank, '_autobook', dict(
            debit=[('deposits', loan)],
            credit=[('loans', loan)],
            text='Principal repayment'))


def truncnorm(lower, upper, sigma):
    return min(max(0, normalvariate((upper - lower) / 2 + lower, sigma)), upper)
