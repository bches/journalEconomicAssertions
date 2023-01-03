"""# Economic Assertions"""

import csv, os

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


if __name__ == '__main__':
    import sys
    filename = '../accounting/DiscountBondPurchase.csv'

    if 'write' in sys.argv:
        with open(filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Input Variables:', 'issuer', 'holder', 'FV', 'PR', 'T', 
                                 'Cash', 'Discount on Bond Payable', 'Bond Payable', 
                                 'Discount on Bond Investment', 'Bond Investment'])
            spamwriter.writerow(['issuer','DR','CR','holder','DR','CR'])
            spamwriter.writerow(['Cash','graphPoint(PR,T)','','Cash','','graphPoint(PR,T)'])
            spamwriter.writerow(['Discount on Bond Payable','graphPoint(FV-PR,T)','','Discount on Bond Investment','','graphPoint(FV-PR,T)'])
            spamwriter.writerow(['Bond Payable','','graphPoint(FV,T)','Bond Investment','graphPoint(FV,T)',''])



    dut = economicAssertion(filename = filename)

    print(dut)
