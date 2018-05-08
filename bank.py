import abcFinance


class Bank(abcFinance.Agent):
    def init(self, reserves=0, loans=0, deposits=0):
        self.make_asset_accounts(['reserves', 'loans'])
        self.make_liability_accounts(['deposits'])
        self.make_flow_accounts(['interest income'])
        #self.make_residual_account('equity')
        self.book(debit=[('reserves', reserves), ('loans', loans)],
                  credit=[('deposits', deposits), ('equity', reserves + loans - deposits)],
                  text='Capital endowment')
        self.book_end_of_period()

    def grant_loan(self):
        _, cash = self.accounts.get_balance('cash')
        _, deposits = self.accounts.get_balance('deposits')
        available_deposits = max(0, cash / 0.1 - deposits)
        offers = self.get_messages('request_loan')
        for offer in offers:
            amount = offer.content
            if amount <= available_deposits:
                self.book(debit=[(what, amount)],
                          credit=[('', amount)],
                         text="buy %s" % what)

