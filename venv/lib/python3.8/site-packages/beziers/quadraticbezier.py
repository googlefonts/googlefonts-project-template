from beziers.segment import Segment
from beziers.line import Line
from beziers.point import Point
from beziers.utils import quadraticRoots, isclose
from beziers.utils.arclengthmixin import ArcLengthMixin

my_epsilon = 2e-7

class QuadraticBezier(ArcLengthMixin,Segment):
  def __init__(self, start, c1,end):
    self.points = [start,c1,end]
    self._range = [0,1]

  def __repr__(self):
    return "B<%s-%s-%s>" % (self[0],self[1],self[2])

  @classmethod
  def fromRepr(klass,text):
    import re
    p = re.compile("^B<(<.*?>)-(<.*?>)-(<.*?>)>$")
    m = p.match(text)
    points = [ Point.fromRepr(m.group(t)) for t in range(1,4) ]
    return klass(*points)

  def pointAtTime(self,t):
    """Returns the point at time t (0->1) along the curve."""
    x = (1 - t) * (1 - t) * self[0].x + 2 * (1 - t) * t * self[1].x + t * t * self[2].x;
    y = (1 - t) * (1 - t) * self[0].y + 2 * (1 - t) * t * self[1].y + t * t * self[2].y;
    return Point(x,y)

  def tOfPoint(self,p):
    """Returns the time t (0->1) of a point on the curve."""
    xroots = quadraticRoots(self[0].x - 2*self[1].x + self[2].x, 2 * (self[1].x-self[0].x), self[0].x - p.x)
    yroots = quadraticRoots(self[0].y - 2*self[1].y + self[2].y, 2 * (self[1].y-self[0].y), self[0].y - p.y)
    if not len(xroots) or not len(yroots):
      return -1
    for x in xroots:
      for y in yroots:
        if -my_epsilon < x - y < my_epsilon:
          return x
    return -1

  def splitAtTime(self,t):
    """Returns two segments, dividing the given segment at a point t (0->1) along the curve."""
    p4 = self[0].lerp(self[1],t)
    p5 = self[1].lerp(self[2],t)
    p7 = p4.lerp(p5,t)
    return (QuadraticBezier(self[0],p4,p7), QuadraticBezier(p7,p5,self[2]))

  def derivative(self):
    """Returns a `Line` representing the derivative of this curve."""
    return Line(
      (self[1]-self[0])*2,
      (self[2]-self[1])*2
    )

  def flatten(self, degree=8):
    samples = self.sample(self.length/degree)
    ss = []
    for i in range(1,len(samples)):
      l = Line(samples[i-1], samples[i])
      l._orig = self
      ss.append(l)
    return ss

  def _findRoots(self,dimension):
    if dimension == "x":
      return quadraticRoots(self[0].x - 2*self[1].x + self[2].x, 2 * (self[1].x-self[0].x), self[0].x)
    elif dimension == "y":
      return quadraticRoots(self[0].y - 2*self[1].y + self[2].y, 2 * (self[1].y-self[0].y), self[0].y)
    else:
      raise "Meh"

  def _findDRoots(self):
    d1 = (self[0].x-2*self[1].x+self[2].x)
    d2 = (self[0].y-2*self[1].y+self[2].y)
    roots = []
    if d1 != 0:
      r1 = (self[0].x-self[1].x)/d1
      roots.append(r1)
    if d2 != 0:
      r2 = (self[0].y-self[1].y)/d2
      roots.append(r2)
    return [ r for r in roots if r >= 0.01 and r <= 0.99 ]

  def findExtremes(self):
    """Returns a list of time `t` values for extremes of the curve."""
    return self._findDRoots()

  @property
  def area(self):
    """Returns the signed area between the curve and the y-axis"""
    return (2*(self[1].x*self[0].y - self[0].x*self[1].y - self[1].x*self[2].y + self[2].x*self[1].y) +
            3*(self[2].x*self[2].y - self[0].x*self[0].y) +
               self[2].x*self[0].y - self[0].x*self[2].y) / 6.

  def toCubicBezier(self):
    """Converts the quadratic bezier to a CubicBezier"""
    from beziers.cubicbezier import CubicBezier
    return CubicBezier(
      self[0], self[0]*(1/3.) + self[1]*(2/3.), self[1]*(2/3.) + self[2]*(1/3.), self[2]
    )
