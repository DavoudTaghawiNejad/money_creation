import abcFinance
from accountingsystem import s
from random import random


class Bank(abcFinance.Agent):
    def init(self, min_capital_ratio, reserves=0, loans=0, deposits=0):
        self.min_capital_ratio = min_capital_ratio
        self.make_asset_accounts(['reserves', 'loans'])
        self.make_liability_accounts(['deposits'])
        self.make_flow_accounts(['interest income'])

        self.book(debit=[('reserves', reserves), ('loans', loans)],
                  credit=[('deposits', deposits), ('equity', reserves + loans - deposits)],
                  text='Capital endowment')
        self.book_end_of_period()

    def announce_interest_rate(self):
        self.interest_rate = random() * 0.1
        return self.interest_rate

    def grant_loans(self):
        side_equity, equity = self.accounts.get_balance('equity')
        total_assets = self.accounts.get_total_assets()
        offers = self.get_messages('request_loan')
        if side_equity != s.DEBIT:
            for offer in offers:
                amount = offer.content
                if equity / (total_assets + amount) >= self.min_capital_ratio:
                    self.make_loan(amount, offer)










    # hide

    def make_loan(self, amount, offer):
        self.book(debit=[('loans', amount)], credit=[('deposits', amount)], text='Loan granting')

        self.send(offer.sender, '_autobook', dict(debit=[('money', amount)],
                                                  credit=[('loans', amount)],
                                                  text='Take out loan'))
