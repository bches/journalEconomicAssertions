# Tools for reading in the various configuration files in the JEA

import csv

def do_csvRead(filename, delimiter=','):
  '''Read a CSV file and return the rows as a list'''
  rows = []
  with open(filename, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
    for row in spamreader:
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

def parseAccountMapping(lines):
  '''Interprest each entry as an account in the JEA
  with the following format:'''
  accounts = [line[0] for line in lines[1:]]
  assert len(accounts) == len(set(accounts)), "Not all account names in account mapping are unique"
  return accounts


