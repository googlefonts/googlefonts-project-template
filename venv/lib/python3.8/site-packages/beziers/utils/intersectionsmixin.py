import sys
from beziers.point import Point
from beziers.utils import isclose
from decimal import Decimal

my_epsilon = 2e-7

class Intersection:
  """An object representing an intersection between two segments.
  The location of the intersection on the first segment is accessible
  as `i.seg1`, `i.t1`. The location of the intersection on the second
  segments is `i.seg2`, `i.t2` and `i.point2` respectively.
  You can get a Point object by calling `i.point`."""

  def __init__(self,seg1,t1,seg2,t2):
    self.seg1   = seg1
    self.t1     = t1
    self.point  = seg1.pointAtTime(t1)
    self.seg2   = seg2
    self.t2     = t2

  def __repr__(self):
    return "I<%s t1=%f t2=%f>" % (self.point, self.t1, self.t2)

class IntersectionsMixin:
  # This isn't something we mix into different classes but I'm
  # just putting it here to keep the code tidy.

  def intersections(self, other, limited = True):
    """Returns an array of `Intersection` objects representing the intersections
    between this Segment and another Segment."""
    # Arrange by degree
    if len(other.points) > len(self.points): self,other = other,self
    if len(self.points) == 4 or len(self.points)==3:
      if len(other.points) == 4 or len(other.points)==3:
        inter = self._curve_curve_intersections(other)
      if len(other.points) == 2:
        inter = self._curve_line_intersections(other)
    elif len(self.points) == 2 and len(other.points) == 2:
        inter = self._line_line_intersections(other)
    else:
      raise ValueError("Couldn't work out which intersection function to use")

    def withinRange(t):
      if t < my_epsilon: return False
      if t > 1.0 + my_epsilon: return False
      return True

    if limited:
      return [ i  for i in inter if withinRange(i.t1) and withinRange(i.t2) ]
    else:
      return inter
    raise "Don't know how to compute intersections of a %s and a %s" % (type(self), type(other))

  def _bothPointsAreOnSameSideOfOrigin(self, a,b,c):
    xDiff = (a.x-c.x) * (b.x-c.x)
    yDiff = (a.y-c.y) * (b.y-c.y)
    return not (xDiff <= 0.0 and yDiff <= 0.0)

  def _line_line_intersections(self, other):
    a = self.start
    b = self.end
    c = other.start
    d = other.end
    if isclose(c.x, d.x) and isclose(a.x, b.x): return []
    if isclose(c.y, d.y) and isclose(a.y, b.y): return []
    if c == d or a == b: return []
    if isclose(b.x,a.x):
      x = a.x
      slope34 = ( d.y - c.y) / ( d.x - c.x )
      y = slope34 * ( x - c.x ) + c.y
      p = Point(x,y)
      i = Intersection(self,self.tOfPoint(p), other, other.tOfPoint(p))
      return [ i ]
    if isclose(c.x,d.x):
      x = c.x
      slope12 = ( b.y - a.y) / ( b.x - a.x )
      y = slope12 * ( x - a.x ) + a.y
      p = Point(x,y)
      i = Intersection(self,self.tOfPoint(p), other, other.tOfPoint(p))
      return [ i ]

    slope12 = ( b.y - a.y) / ( b.x - a.x )
    slope34 = ( d.y - c.y) / ( d.x - c.x )
    if abs(slope12 - slope34) < my_epsilon: return [ ]
    x = ( slope12 * a.x - a.y - slope34 * c.x + c.y ) / ( slope12 - slope34 )
    y = slope12 * ( x - a.x ) + a.y
    intersection = Point(x,y)
    if (self._bothPointsAreOnSameSideOfOrigin(intersection, b, a) and self._bothPointsAreOnSameSideOfOrigin(intersection, c, d)):
      return [ Intersection(self,self.tOfPoint(intersection, its_on_the_line_i_swear=True), other, other.tOfPoint(intersection, its_on_the_line_i_swear=True)) ]
    return []

  def _curve_line_intersections_t(self,line):
    t = line.alignmentTransformation()
    c1 = self.transformed(t)
    intersections = c1._findRoots("y")
    return sorted(intersections)

  def _curve_line_intersections(self,line):
    inter = []
    for t in self._curve_line_intersections_t(line):
      inter.append(Intersection(self,t,line,line.tOfPoint(self.pointAtTime(t), its_on_the_line_i_swear=True)))
    return inter

  def _curve_curve_intersections_t(self,other, precision=1e-3):
    assert(len(self.points) > 2 and len(other.points) > 2)
    if not (self.bounds().overlaps(other.bounds())): return []
    if self.bounds().area < precision and other.bounds().area < precision:
      return [ [
      0.5*(self._range[0] + self._range[1]),
      0.5*(other._range[0] + other._range[1]),
     ] ]
    def xmap(v,ts,te): return ts+(te-ts)*v
    c11, c12 = self.splitAtTime(0.5)
    c11._range = [ self._range[0], xmap(0.5,self._range[0],self._range[1])]
    c12._range = [ xmap(0.5,self._range[0],self._range[1]), self._range[1]]
    c21, c22 = other.splitAtTime(0.5)
    c21._range = [ other._range[0], xmap(0.5,other._range[0],other._range[1])]
    c22._range = [xmap(0.5,other._range[0],other._range[1]), other._range[1]]
    assert(c11._range[0] < c11._range[1])
    assert(c12._range[0] < c12._range[1])
    assert(c21._range[0] < c21._range[1])
    assert(c22._range[0] < c22._range[1])

    found = []
    for this in [c11,c12]:
      for that in [c21,c22]:
        if this.bounds().overlaps(that.bounds()):
          found.extend(this._curve_curve_intersections_t(that, precision))
    seen = {}
    numPrecisionDigits = abs(Decimal(str(precision)).as_tuple().exponent)

    def filterSeen(n):
      # use (precision - 1) digits to check whether we have already
      # seen this value
      key = f"%.{numPrecisionDigits - 1}f" % n[0]

      if key in seen: return False
      seen[key] = 1
      return True
    found = filter(filterSeen, found)
    return found

  def _curve_curve_intersections(self,other):
    assert(len(self.points) > 2 and len(other.points) > 2)
    return [Intersection(self,t[0],other,t[1]) for t in self._curve_curve_intersections_t(other)]
