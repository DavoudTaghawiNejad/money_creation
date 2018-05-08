import abcFinance
from random import randrange


class Household(abcFinance.Agent):
    def init(self, money=0, loans=0, participations=0):
        self.make_asset_accounts(['money','participations'])
        self.make_liability_accounts(['loans'])
        self.make_flow_accounts(['dividend income','interest expenses'])
        # self.make_residual_account('equity')
        self.book(debit=[('money', money), ('participations', participations)],
                  credit=[('loans', loans), ('equity', money + participations - loans)],
                  text='Initial endowment')
        self.book_end_of_period()

    def request_loans(self):
        bank = ('bank', 0)
        self.send(bank, 'request_loan', randrange(10, 100))

    def pay_interest(self):
        bank = ('bank', 0)
        interest_message = self.get_messages('interest_rate')
        if interest_message:
            interest_rate = interest_message[0].content
            self.interest_rate = interest_rate
        else:
            interest_rate = self.interest_rate
        _, loan = self.accounts['loans'].get_balance()
        interest_payment = loan * interest_rate
        self.book(debit=[('interest expenses', interest_payment)],
                  credit=[('money', interest_payment)],
                  text='Interest payment')

        self.send(bank, '_autobook', dict(
            debit=[('deposits', interest_payment)],
            credit=[('interest income', interest_payment)],
            text='Interest payment'))

    def repay_loan_principal(self):
        bank = ('bank', 0)
        _, loan = self.accounts['loans'].get_balance()

        self.book(debit=[('loans', loan)], credit=[('money', loan)], text='Principal repayment')
        self.send(bank, '_autobook', dict(
            debit=[('deposits', loan)],
            credit=[('loans', loan)],
            text='Principal repayment'))
