import math

class Point(object):
  """A representation of a point within the Beziers world.

  Here are some things you can do with points. You can interpret
  them as vectors, and add them together::

    >>> a = Point(5,5)
    >>> b = Point(10,10)
    >>> a + b
    <15.0,15.0>

  You can multiply them by a scalar to scale them::

    >>> a * 2
    <10.0,10.0>

  You can adjust them::

    >>> a += b
    >>> a
    <15.0,15.0>

  If you're using Python 3, you can abuse operator overloading
  and compute the dot product of two vectors:

    >>> a = Point(5,5)
    >>> b = Point(10,10)
    >>> a @ b
    100.0

"""

  def __init__(self, x,y):
    self.x = float(x)
    self.y = float(y)

  def __repr__(self):
    return "<%s,%s>" % (self.x,self.y)

  @classmethod
  def fromRepr(klass,text):
    import re
    p = re.compile("^<([^,]+),([^>]+)>$")
    m = p.match(text)
    return klass(m.group(1), m.group(2))

  def __eq__(self, other):
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
      return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    return isclose(self.x, other.x) and isclose(self.y, other.y)

  def __hash__(self):
    return  hash(self.x) << 32 ^ hash(self.y)

  def __mul__(self, other):
    """Multiply a point by a scalar."""
    return Point(self.x * other, self.y * other)

  def __div__(self, other):
    return Point(self.x / other, self.y / other)

  def __truediv__(self, other):
    return Point(self.x / other, self.y / other)

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def __iadd__(self, other):
    self.x += other.x
    self.y += other.y
    return self

  def __isub__(self, other):
    self.x -= other.x
    self.y -= other.y
    return self

  def __matmul__(self,other): # Dot product. Abusing overloading. Sue me.
    return self.dot(other)

  def dot(self, other):
    return self.x * other.x + self.y * other.y

  def clone(self):
    """Clone a point, returning a new object with the same co-ordinates."""
    return Point(self.x,self.y)

  def rounded(self):
    """Return a point with the co-ordinates truncated to integers"""
    return Point(int(self.x),int(self.y))

  def lerp(self, other, t):
    """Interpolate between two points, at time t."""
    return self * (1-t) + other * (t)

  @property
  def squareMagnitude(self):
    """Interpreting this point as a vector, returns the squared magnitude (Euclidean length) of the vector."""
    return self.x*self.x + self.y*self.y

  @property
  def magnitude(self):
    """Interpreting this point as a vector, returns the magnitude (Euclidean length) of the vector."""
    return math.sqrt(self.squareMagnitude)

  def toUnitVector(self):
    """Divides this point by its magnitude, returning a vector of length 1."""
    mag = self.magnitude
    if mag == 0.0: mag = 1.0
    return Point(self.x/mag, self.y/mag)

  @property
  def angle(self):
    """Interpreting this point as a vector, returns the angle in radians of the vector."""
    return math.atan2(self.y,self.x)

  @property
  def slope(self):
    """Returns slope y/x"""
    if self.x == 0: return 0
    return self.y / self.x

  @classmethod
  def fromAngle(self,angle):
    """Given an angle in radians, return a unit vector representing that angle."""
    return Point(math.cos(angle), math.sin(angle)).toUnitVector()

  def rotated(self,around,by):
    """Return a new point found by rotating this point around another point, by an angle given in radians."""
    delta = around - self
    oldangle = delta.angle
    newangle = oldangle + by
    unitvector = Point.fromAngle(newangle)
    new = around - unitvector * delta.magnitude
    return new

  def rotate(self,around,by):
    """Mutate this point by rotating it around another point, by an angle given in radians."""
    new = self.rotated(around, by)
    self.x = new.x
    self.y = new.y

  def squareDistanceFrom(self,other):
    """Returns the squared Euclidean distance between this point and another."""
    return (self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y)

  def distanceFrom(self,other):
    """Returns the Euclidean distance between this point and another."""
    return math.sqrt(self.squareDistanceFrom(other))

  def transformed(self, transformation):
    m = transformation.matrix
    x, y = self.x, self.y
    a1, a2, b1 = m[0]
    a3, a4, b2 = m[1]
    xPrime = a1 * x + a2 * y + b1
    yPrime = a3 * x + a4 * y + b2
    return Point(xPrime, yPrime)

  def transform(self, transformation):
    new = self.transformed(transformation)
    self.x = new.x
    self.y = new.y
