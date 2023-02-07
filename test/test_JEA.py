import sys
sys.path.append('../src')
from JEAdata import JEA
from tools.tvom import pv, pva

if __name__ == '__main__':
    dut = JEA(Nperiods=15)
    print(dut)
    
    dut.addAssertion(filename = '../accounting/DiscountBondPurchase.csv')

    # Face value of the bond is $100,000
    FV = 100e3

    # The stated rate of the bond is 3% per period
    iSR = 0.03

    # Number of periods
    N = 14
    
    # The payment each period is the stated rate times the face value
    P = iSR * FV

    # The bond is purchased at a discount with an interest rate of 2%
    iM = 0.04
    PR = FV * pv(iM, N) + P * pva(iM, N)

    # the bond is divided into 5 tranches, $20,000 each
    T = 5
    
    dut.doAssertion(assertionName='DiscountBondPurchase', k=0,
                    args={'T':T, 'FV':FV/T, 'PR':PR/T,
                          'issuer':1, 'holder':2,
                          'Cash':1, 'Discount on Bond Payable':2,
                          'Bond Payable':3, 'Bond Investment':4,
                          'Discount on Bond Investment':5})
    
    print(dut)
