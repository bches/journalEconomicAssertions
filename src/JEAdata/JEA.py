"""# JEA base class"""

import re
import csv, os

class graphPoint:
  def __init__(self, price_per_unit=0, number_of_units=1):
    if isinstance(price_per_unit, str):
      s = re.split("@", price_per_unit)
      self.N = int(s[0])
      try:
        self.P = float(s[1])
      except IndexError:
        self.N = 1
        self.P = float(s[0])
    else:
      self.P = price_per_unit
      self.N = number_of_units

  def value(self):
    return self.N * self.P
      
  def __repr__(self):
    return '%s @ x%s' % (self.N, self.P)

  def __add__(self, other):
    V = self.value() + other.value()
    return graphPoint(V, 1)

  def __iadd__(self, other):
    return self + other

  def __sub__(self, other):
    V = self.value() - other.value()
    return graphPoint(V, 1)

  def __isub__(self, other):
    return self - other

  def nonzero(self):
    return self.N != 0 and self.P != 0

  def iszero(self):
    return not self.nonzero()

class flowGraph:
  '''A directed graph of ordered points.
  Each flow of the graph is from one two-dimensional
  object to another.
  '''
  def __init__(self, Nperiods):
    self.points = [None]*Nperiods

  def __len__(self):
    return len(self.points)

  def __repr__(self):
    return str(self.points)

  def __iter__(self):
    for k in range(len(self)):
      self.balances(k)
      yield k

  def __getitem__(self, k):
    return self.points[k]

  def getPoint(self, k, _fromNode, _toNode):
    p = self.points[k]
    if p == None:
      return graphPoint()
    for f, t, a in p:
      if f == _fromNode and t == _toNode:
        return a
    raise IndexError('Node not found: %d, %s, %s' % (k,_fromNode, _toNode) )

  def addFlow(self, k, _fromNode, _toNode, value):
    '''addFlow(self, k, _fromNode, _toNode, value)
    Add flow from point _fromNode to point _toNode 
    of value value in period k to the graph.
    k: integer
    _fromNode: length-2 tuple (x,y)
    _toNode: length-2 tuple (x,y)
    value: graphPoint(P,N)
    '''
    assert len(_fromNode) == 2, "_fromNode must be length 2"
    assert len(_toNode) == 2, "_toNode must be length 2"
    assert type(value) == type(graphPoint()), "value must be type graphPoint"
    if value.iszero():
      return
    assert k < len(self), "k must be less than the length of the graph"
    try:
      self.points[k].append((_fromNode, _toNode, value))
    except AttributeError:
      self.points[k] = [(_fromNode, _toNode, value)]

  def inflows(self, k):
    '''Calculate all of the inflows to each node in period k'''
    retVal = {}
    if self.points[k] == None:
      return retVal
    for (fromNode, toNode, amount) in self.points[k]:
      try:
        retVal[toNode] += amount
      except KeyError:
        retVal[toNode] = amount
    return retVal

  def outflows(self, k):
    '''Calculate all of the outflows from each node in period k'''
    retVal = {}
    if self.points[k] == None:
      return retVal
    for (fromNode, toNode, amount) in self.points[k]:
      try:
        retVal[fromNode] += amount
      except KeyError:
        retVal[fromNode] = amount
    return retVal

  def balances(self, k):
    '''Calculate the balances at period k and store along the diagonal.
    Balances are calculated as inflows - outflows.
    '''
    ins = self.inflows(k)
    outs = self.outflows(k)
    allNodes = set(ins.keys()).union(set(outs.keys()))
    for each in allNodes:
      if k == 0:
        previousBalance = graphPoint()
      else:
        try:
          previousBalance = self.getPoint(k-1, each, each)
        except IndexError:
          previousBalance = graphPoint()
      try:
        inAmt = ins[each]
      except KeyError:
        inAmt = graphPoint()
      try:
        outAmt = outs[each]
      except KeyError:
        outAmt = graphPoint()
      self.addFlow(k, each, each, previousBalance + inAmt - outAmt)

  def addFromArray(self, k, fromNode, toNode, valueArray, skip=None):
    '''addFromArray(self, k, fromNode, toNode, valueArray, skip=None)
    k: insert into graph starting with this period
    fromNode: for all of the entries
    toNode: for all of the entries
    valueArray: array of prices, units will be 1
    skip: number of periods to skip between array entries, if None, don't skip any
    '''
    for i in range(len(valueArray)):
      if skip == None:
        self.addFlow(k+i, fromNode, toNode, graphPoint(valueArray[i],1))
      else:
        self.addFlow(k+i*skip, fromNode, toNode, graphPoint(valueArray[i],1))

def do_csvRead(filename):
  '''Read a CSV file and return the rows as a list'''
  rows = []
  with open(filename, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
      print('row=',row)
      rows += [row]
  return rows

def parseJournalEntries(links):
  '''Interpret each entry in the list of strings, links, as two side-by-side
  journal entries indicating that the doubly-entry accounting on the left
  flows over to the double-entry accounting on the right.  Check to make sure
  each line balances out.'''
  entity1 = links[1][0]
  entity2 = links[1][3]
  s = []
  for link in links[2:]:
    (acct1, dr1, cr1, acct2, dr2, cr2) = tuple(link[:6])
    assert (len(dr1)==0) ^ (len(cr1)==0), "One debit or credit per line, but not both"
    assert (len(dr2)==0) ^ (len(cr2)==0), "One debit or credit per line, but not both"
    assert (len(dr1)==0) ^ (len(dr2)==0), "Debit on one entity must go to credit on the other"
    assert (len(cr1)==0) ^ (len(cr2)==0), "Debit on one entity must go to credit on the other"
    if len(cr1) > 0:
      fromPt = (entity1, acct1)
      toPt = (entity2, acct2)
      assert cr1 == dr2, "Line not balanced"
      amount = cr1
    elif len(cr2) > 0:
      fromPt = (entity2, acct2)
      toPt = (entity1, acct1)
      assert cr2==dr1, "Line not balanced"
      amount = cr2
    else:
      assert False, "Could not determine from/to: %s" % link
    s += [(fromPt, toPt, amount)]
  return s


class economicAssertion:
  def __init__(self, filename):
    (head, tail) = os.path.split(filename)
    (root, ext) = os.path.splitext(tail)
    self.name = root

    if ext == ".csv":
      entries = do_csvRead(filename)
    elif ext == ".toml":
      assert False, "TOML not yet implemented."
    else:
      assert False, "Unrecognized file extension: %s" % ext
    
    self.methods = []
    self.input_variables = entries[0][1:]
    for each in parseJournalEntries(entries):
      (_fromNode, _toNode, value) = each
      self.methods += ['self.G.addFlow(k, %s, %s, %s)' % (_fromNode, _toNode, value)]

  def __repr__(self) -> str:
    args = ','.join(self.input_variables)
    s = "%s(%s):\n" % (self.name, args)
    s += '\n'.join(map(str, self.methods))
    return s

  def __iter__(self):
    for each in self.methods:
      yield each

  def getInputVariables(self):
    return self.input_variables 

        
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
  
  dut.addAssertion(filename = '../../accounting/DiscountBondPurchase.csv')
  dut.doAssertion(assertionName='DiscountBondPurchase', k=0,
                  args={'T':7, 'FV':60, 'PR':50, 'issuer':1, 'holder':2,
                        'Cash':1, 'Discount on Bond Payable':2,
                        'Bond Payable':3, 'Bond Investment':4,
                        'Discount on Bond Investment':5})
  
  print(dut)

