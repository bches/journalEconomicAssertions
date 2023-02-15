import re

class graphPoint:
  def __init__(self, price_per_unit=0, number_of_units=1):
    if isinstance(price_per_unit, str):
      s = re.split("@", price_per_unit)
      self.N = int(s[0])
      try:
        self.P = float(s[1])
      except IndexError:
        self.N = 1
        self.P = float(s[0])
    else:
      self.P = price_per_unit
      self.N = number_of_units

  def __repr__(self):
    return '%s @ x%s' % (self.N, self.P)

  def __add__(self, other):
    V = self.P * self.N + other.P * other.N
    return graphPoint(V, 1)

  def __iadd__(self, other):
    return self + other

  def __sub__(self, other):
    V = self.P * self.N - other.P * other.N
    return graphPoint(V, 1)

  def __isub__(self, other):
    return self - other

  def nonzero(self):
    return self.N != 0 and self.P != 0

  def iszero(self):
    return not self.nonzero()

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

