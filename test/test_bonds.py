import sys
sys.path.append('../src')
from assertions import bond 
from JEAbooks.JEAbooks import JEAbooks

if __name__ == '__main__':
    # issuer creates the intent to enter into a bond agreement.
    # The bond is split into 10 tranches of 100,000 each.
    # The bond lasts for 6 periods, with no time in between
    # periods (L=0).  The stated rated of the 6% per period.

    accounts = {'Cash':1, 'Bond Payable':2,
                'Bond Investment':3,
                'Discount on Bond Payable':4,
                'Discount on Bond Investment':5,
                'Premium on Bond Payable':8,
                'Premium on Bond Investment':9,
                'Interest Expense':6,
                'Interest Revenue':7}

    print('At issue:')
    N = 6
    dut = bond(issuer=1, FV=100e3, T=10, N=N, L=0, iSR=0.06,
               accounts=accounts, dir='../accounting')
    print(dut,'\n')

    # create the books for the JEA record keeping
    books = JEAbooks(Nperiods=10,
                     acctMap_filename='../accounting/accountMapping.csv')
    
    # holder purchases 7 tranches of the bond when the market
    # rate is 7% perperiod.
    print('At purchase:')
    dut(G=books.G, k=0, holder=2, iM=0.07, Tp=7)

    # check the books
    print()
    print('books.G =', books.G)

    # amortization:
    print('\n amortization:')
    for i in range(1,N+1):
        print('\t%d: %s' % (i, books.G[i]))

    print()
    print('Testing at Face value...')
    N = 6
    dut = bond(issuer=1, FV=100e3, T=10, N=N, L=0, iSR=0.06,
               accounts=accounts, dir='../accounting')
    print(dut,'\n')

    # create the books for the JEA record keeping
    books = JEAbooks(Nperiods=10,
                     acctMap_filename='../accounting/accountMapping.csv')
    
    # holder purchases 7 tranches of the bond when the market
    # rate is 6% per period.
    print('At purchase:')
    dut(G=books.G, k=0, holder=2, iM=0.06, Tp=7)

    # check the books
    print()
    print('books.G =', books.G)

    print()
    print('At a premium...')
    N = 6
    dut = bond(issuer=1, FV=100e3, T=10, N=N, L=0, iSR=0.06,
               accounts=accounts, dir='../accounting')
    print(dut,'\n')

    # create the books for the JEA record keeping
    books = JEAbooks(Nperiods=10,
                     acctMap_filename='../accounting/accountMapping.csv')
    
    # holder purchases 7 tranches of the bond when the market
    # rate is 5% per period.
    print('At purchase:')
    dut(G=books.G, k=0, holder=2, iM=0.05, Tp=7)

    # check the books
    print()
    print('books.G =', books.G)

    # amortization:
    print('\n amortization:')
    for i in range(1,N+1):
        print('\t%d: %s' % (i, books.G[i]))
