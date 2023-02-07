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

    print('\n\tTesting nested...')
    nested = graphPoint(price_per_unit=c, number_of_units=2)
    print('nested c @ 2 =', nested)

    nested = graphPoint(price_per_unit=2, number_of_units=c)
    print('nested 2 @ c =', nested)

    nested = graphPoint(price_per_unit=c, number_of_units=b)
    print('nested c @ b =', nested)

    print('Add a @ 2 to 2 @ b, should be 4*(a+b)...')
    nested1 = graphPoint(price_per_unit=a, number_of_units=2)
    nested_sum = nested + nested1
    print('nested_sum =', nested_sum)
    
