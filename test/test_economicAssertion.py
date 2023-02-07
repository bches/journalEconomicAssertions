import sys
sys.path.append('../src')
from JEAdata import economicAssertion


if __name__ == '__main__':
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
