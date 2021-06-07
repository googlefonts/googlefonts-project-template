from math import sqrt
try:
    from math import isclose
except ImportError:
    def isclose(a, b):
        return -1e-9 < a - b < 1e-9

def quadraticRoots(a, b, c):
  """Returns real roots of at^2 + bt + c = 0 if 0 < root < 1"""
  roots = []
  if a != 0.0 and b*b-4*a*c > 0.0:
    x = -b / (2 * a)
    y = sqrt(b*b - 4*a*c) / (2*a)
    t1 = x - y
    if 0.0 <= t1 <= 1.0:
      roots.append(t1)
    t2 = x + y
    if 0.0 <= t2 <= 1.0:
      roots.append(t2)
  return roots

