import sys
sys.path.append('../src')
from JEAdata import graphPoint, flowGraph

if __name__ == '__main__':
    G = flowGraph(5)
    a = graphPoint(7, 2)
    b = graphPoint(1.5, 4)
    
    G.addFlow(1, (1,1), (2,3), a)
    G.addFlow(1, (3,4), (2,3), b)
    print('G:',G)
    
    retVal = G.inflows(1)
    print('inflows:', retVal)
    
    retVal = G.outflows(1)
    print('outflows:', retVal)
    
    print()
    G.addFlow(2, (5,1), (1,1), graphPoint(1.0, 10))
    print('G=',G)
    print()
    
    print()
    import numpy as np
    print('addFlow from an array')
    ar = np.array([11, 13])
    
    G.addFromArray(k=3, fromNode=(1,1), toNode=(5,1), valueArray=ar)
    
    print('balances:')
    for period in G:
        print('\t%d: %s' % (period, G[period]))
