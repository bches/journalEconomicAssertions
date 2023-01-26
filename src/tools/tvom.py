# Time Value of Money tools

def pv(i, N):
    '''The present value of $1 N periods into the future at
    interest rate, i'''
    return (1 + i) ** (-N)

def pva(i, N):
    '''The present value of an annuity N periods into the future at
    interest rate, i, with payment at the end of the period.'''
    return (1 - pv(i, N)) / i

