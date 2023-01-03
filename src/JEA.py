"""# JEA base class"""

import re
from flow_graph import flowGraph
from economic_assertion import economicAssertion
from graph_point import graphPoint

class JEA():
  def __init__(self, Nperiods):
    '''The base class of the journal of economic assertions,
    from which more specifically-tailored classes are derived.
    Nperiods: total of number of periods to journal.'''
    self.G = flowGraph(Nperiods)
    self.assertions = {}

  def __repr__(self):
    s = '<Instance of %s at %s:\n' % (self.__class__.__name__, id(self))
    s += '\tG = %s,\n' % self.G
    s += '\tassertions = %s\n>' % self.assertions
    return s

  def __iter__(self):
    for period in self.Nperiods:
      self.current = period
      self.lock()
      self.G.balances()
      self.reconcile()
      self.unlock()
      yield

  def lock(self):
    '''Virtual method to override to lock a set of transactions to process'''
    pass

  def unlock(self):
    '''Virtual method to override to undo lock()'''
    pass

  def reconcile(self):
    '''Virtual method to override to reconcile accounts with a negative balance.'''
    pass

  def addAssertion(self, filename):
    a = economicAssertion(filename)
    self.assertions[a.name] = a

  def doAssertion(self, assertionName, k, args):
    a = self.assertions[assertionName]
    vars = a.getInputVariables()
    for line in a:
      #print('line=',line)
      s = re.sub('k', str(k), line)
      for v in vars:
        #print('\tv=',v)
        s = re.sub(v, str(args[v]), s)
      print('s=',s)
      ret = eval(s)
  
  def periodicPayment(self, k, payer, payee, Amort, Interest, Cash, 
                      InterestRevenue, InterestExpense, 
                      AmortAcct_payee, AmortAcct_payer):
    self.G.addFlow(k, (payer, Cash), (payee, Cash), Amort + Interest)
    self.G.addFlow(k, (payee, InterestRevenue), (payer, InterestExepense), Interest)
    self.G.addFlow(k, (AmortAcct_payee), (AmortAcct_payer), Amort)
    # need to fix the above for a Premium bond


if __name__ == '__main__':
    dut = JEA(Nperiods=10)
    print(dut)
    
    dut.addAssertion(filename = '../accounting/DiscountBondPurchase.csv')
    dut.doAssertion(assertionName='DiscountBondPurchase', k=0,
                    args={'T':7, 'FV':60, 'PR':50, 'issuer':1, 'holder':2,
                          'Cash':1, 'Discount on Bond Payable':2,
                          'Bond Payable':3, 'Bond Investment':4,
                          'Discount on Bond Investment':5})
    
    print(dut)

