import sys
sys.path.append('../src')
from JEAdata import JEAdata

if __name__ == '__main__':
  dut = JEAdata(Nperiods=10,
                acctMap_filename='../accounting/accountMapping.csv')
  print(dut)
    
