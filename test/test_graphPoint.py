import sys
sys.path.append('../src')
from JEAdata import graphPoint


if __name__ == '__main__':
    a = graphPoint(7, 2)
    b = graphPoint(1.5, 4)
    print('a=',a)
    print('b=',b)
    print()
    print('a+b=', a+b)
    print('a-b=', a-b)

    c = graphPoint('29@3')
    print('c=',c)

    d = graphPoint('4096')
    print('d=',d)

    print('c+d=',c+d)

    print('\nMultiply...')
    print('a * 2 =', a*2)
    
    print('\n\tTesting nested...')
    nested = graphPoint(price_per_unit=c, number_of_units=2)
    print('nested c @ 2 =', nested)

    nested = graphPoint(price_per_unit=2, number_of_units=c)
    print('nested 2 @ c =', nested)

    nested = graphPoint(price_per_unit=c, number_of_units=b)
    print('nested c @ b =', nested)
    
    print('Add a @ 2 to 2 @ b, should be 2*(a+b)...')
    nested2 = graphPoint(price_per_unit=b, number_of_units=2)
    nested1 = graphPoint(price_per_unit=2, number_of_units=a)
    print('nested1=',nested1)
    print('nested2=',nested2)
    nested_sum = nested2 + nested1
    print('nested_sum =', nested_sum)
    print('(a+b)*2=',(a+b)*2)

    x = graphPoint(price_per_unit=3, number_of_units=15)
    y = graphPoint(price_per_unit=9, number_of_units=5)

    print('\nEquivalence')
    print('x == y:', x == y)
