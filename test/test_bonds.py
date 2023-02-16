import sys
sys.path.append('../src')
from assertions import bond 


if __name__ == '__main__':
    dut = bond(issuer=1, FV=60e3, T=7, N=5, L=2, iSR=0.05,
               accounts = {'Cash':1, 'Bond Payable':2,
                           'Bond Investment':3,
                           'Discount on Bond Payable':4,
                           'Discount on Bond Investment':5,
                           'Interest Expense':6,
                           'Interest Revenue':7},
               dir='../accounting')
    print(dut)

    dut(k=0, holder=2, iM=0.06, Tp=3)
    print(dut)
