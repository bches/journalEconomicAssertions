import sys
sys.path.append('../src')
from JEAdata import economicAssertion


if __name__ == '__main__':
    purchase = economicAssertion(filename = '../accounting/DiscountBondPurchase.csv')
    purchase.addInputVariable('iM')
    print(purchase)

    payments = economicAssertion(filename = '../accounting/DiscountBondPeriodicPayment.csv')
    payments.addInputVariable('iSR')
    print(payments)

    repayment = economicAssertion(filename = '../accounting/DiscountBondRepayment.csv')
    print(repayment)
