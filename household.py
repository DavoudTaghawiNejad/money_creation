import abcFinance


class Household(abcFinance.Agent):
    def init(self, money=0, loans=0, participations=0):
        self.make_asset_accounts(['money','participations'])
        self.make_liability_accounts(['loans'])
        self.make_flow_accounts(['dividend income','interest expenses'])
        #self.make_residual_account('equity')
        self.book(debit=[('money', money),('participations', participations)],
                  credit=[('loans', loans), ('equity', money + participations - loans)],
                  text='Initial endowment')
        self.book_end_of_period()

    def deposit_money(self, bank, amount):
        self.send(bank, '_autobook', dict(debit=[('cash', amount)],
                                          credit=[('deposits', amount)],
                                          text='deposit cash'))
        self.book(debit=[('deposits', amount)],
                  credit=[('cash', amount)],
                  text='deposits cash')

    def get_loan(self, bank, amount):
        self.send(bank, 'request_loan', amount)
