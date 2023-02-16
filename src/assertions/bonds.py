# Economic assertions associated with bonds

from JEAdata.JEAdata import economicAssertion
from tools.tvom import pv, pva

class bond(economicAssertion):
  '''Class to implement the full accounting life cycle of a
  bond purchased at a discoiunt, premium or face vale.
  Derived from economicAssertion base class.'''

  def __init__(self, issuer, FV, T, N, L, iSR, accounts, dir = '../../accounting'):
    '''issuer issues a bond to be purchased
    FV: Face value of the bond per tranche
    T: number of tranches purchased
    N: number of payment periods
    L: number of periods in between payments
    iSR: stated rate
    accounts: dictionary of the accounts for recording the bond
    '''
    self.T = T
    self.args = {'issuer':issuer, 'FV':FV, 'N':N, 'L':L, 'iSR':iSR}
    self.input_variables = self.args.keys()
    self.methods = ['purchase', 'payments', 'repayment']
    self.discount = {'purchase':economicAssertion(filename = dir+'/DiscountBondPurchase.csv'),
                     'payments':economicAssertion(filename = dir+'/DiscountBondPeriodicPayment.csv'),
                     'repayment':economicAssertion(filename = dir+'/DiscountBondRepayment.csv')}
#    self.premium = {'purchase':economicAssertion(filename = dir+'/PremiumBondPurchase.csv'),
#                     'payments':economicAssertion(filename = dir+'/PremiumBondPeriodicPayment.csv'),
#                     'repayment':economicAssertion(filename = dir+'/PremiumBondRepayment.csv')}
#    self.face = {'purchase':economicAssertion(filename = dir+'/FaceBondPurchase.csv'),
#                     'payments':economicAssertion(filename = dir+'/FaceBondPeriodicPayment.csv'),
#                     'repayment':economicAssertion(filename = dir+'/FaceBondRepayment.csv')}
    self.bondType = None
    self.accounts = accounts

  def __call__(self, k, holder, iM, Tp):
    '''The bond is purchased and the issuer and holder jointly attest to the
    economic transaction of the bond.  All journal entries associated with the
    life cycle of the bond are recorded for both parties.
    holder purchases Tp tranches of the bond at market rate, iM'''
    assert Tp <= self.T, "Not enough tranches (avail=%d, tried to purchase %d)" % (self.T, Tp)
    FV = self.args['FV']
    iSR = self.args['iSR']
    N = self.args['N']
    P = FV * iSR
    PR = FV * pv(iM, N) + P * pva(iM, N)

    args = {}
    args.update(self.args)
    args.update(self.accounts)
    args.update({'holder':holder, 'T':Tp, 'PR':PR})
    if FV > PR:
      bondType = 'Discount'
      self.discount['purchase'](k=k, args=args)
      for i in range(N):
        self.discount['payments'](k=k, args=args)
      self.discount['repayment'](k=k, args=args)
    elif PR > FV:
      bondType = 'Premium'
      self.premium['purchase'](k=k, args=args)
      for i in range(N):
        self.premium['payments'](k=k, args=args)
      self.premium['repayment'](k=k, args=args)
    else:
      bondType = 'Face'
      self.face['purchase'](k=k, args=args)
      for i in range(N):
        self.face['payments'](k=k, args=args)
      self.face['repayment'](k=k, args=args)

    # decrement tranches available
    self.T -= Tp
      
