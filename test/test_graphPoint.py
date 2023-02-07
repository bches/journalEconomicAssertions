import sys
sys.path.append('../src')
from JEAdata import graphPoint


if __name__ == '__main__':
    a = graphPoint(7, 2)
    b = graphPoint(1.5, 4)
    print('a+b=', a+b)
    print('a-b=', a-b)

    c = graphPoint('29@3')
    print('c=',c)

    d = graphPoint('4096')
    print('d=',d)

    print('c+d=',c+d)
