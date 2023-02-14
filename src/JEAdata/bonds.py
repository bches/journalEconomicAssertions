class bond(economicAssertion):
  '''Class to implement the full accounting life cycle of a
  bond purchased at a discoiunt, premium or face vale.
  Derived from economicAssertion base class.'''

  def __init__(self, issuer, FV, T, N, L, iSR):
    '''issuer issues a bond to be purchased
    FV: Face value of the bond per tranche
    T: number of tranches purchased
    N: number of payment periods
    L: number of periods in between payments
    iSR: stated rate
    issuer_accts: dictionary of the issuer's accounts for recording the bond
    '''
    self.args = {'issuer':issuer, 'FV':FV, 'T':T, 'N':N, 'L':L, 'iSR':iSR}
    self.discount = {'purchase':economicAssertion(filename = '/content/drive/My Drive/DiscountBondPurchase.csv'),
                     'payment':economicAssertion(filename = '/content/drive/My Drive/DiscountBondPeriodicPayment.csv'),
                     'repayment':economicAssertion(filename = '/content/drive/My Drive/DiscountBondRepayment.csv')}
    self.accounts = {}

  def __call__(self, k, holder, iM):
    '''The bond is purchases and the issuer and holder jointly attest to the
    economic transaction of the bond.  All journal entries associated with the
    life cycle of the bond are recorded for both parties.'''
    FV = self.args['FV']
    iSR = self.args['iSR']
    N = self.args['N']
    P = FV * iSR
    PR = FV * pv(iM, N) + P * pva(iM, N)

    args = {each:self.accounts[each] for each in ['Cash', 'Bond Investment', 'Bond Payable']}
    args.update({'issuer':issuer, 'holder':holder, 'FV':FV, 'T':T, 'PR':PR})
    if FV > PR:
      args.update({each:self.accounts[each] for each in ['Discount on Bond Investment', 'Discount on Bond Payable']})
      bondType = 'Discount'
      self.discount['purchase'](k=k, args=args)
    elif PR > FV:
      bondType = 'Premium'
    else:
      bondType = 'Face'

    args = {each:self.accounts[each] for each in ['Cash', 'Interest Revenue', 'Interest Expense']}
    for i in range(N):
      if bondType == 'Discount':
        self.discount['payment']()

    args = {each:self.accounts[each] for each in ['Cash', 'Bond Investment', 'Bond Payable']}
    if bondType == 'Discount':
      self.discount['repayment']

