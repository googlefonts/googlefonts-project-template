from beziers.segment import Segment
from beziers.line import Line
from beziers.point import Point
from beziers.quadraticbezier import QuadraticBezier
from beziers.utils.arclengthmixin import ArcLengthMixin

import math
from beziers.utils.legendregauss import Tvalues, Cvalues
from beziers.utils import quadraticRoots

class CubicBezier(ArcLengthMixin,Segment):
  def __init__(self, start, c1,c2,end):
    self.points = [start,c1,c2,end]
    self._range = [0,1]

  def __repr__(self):
    return "B<%s-%s-%s-%s>" % (self[0],self[1],self[2],self[3])

  @classmethod
  def fromRepr(klass,text):
    import re
    p = re.compile("^B<(<.*?>)-(<.*?>)-(<.*?>)-(<.*?>)>$")
    m = p.match(text)
    points = [ Point.fromRepr(m.group(t)) for t in range(1,5) ]
    return klass(*points)

  def pointAtTime(self,t):
    """Returns the point at time t (0->1) along the curve."""
    x = (1 - t) * (1 - t) * (1 - t) * self[0].x + 3 * (1 - t) * (1 - t) * t * self[1].x + 3 * (1 - t) * t * t * self[2].x + t * t * t * self[3].x;
    y = (1 - t) * (1 - t) * (1 - t) * self[0].y + 3 * (1 - t) * (1 - t) * t * self[1].y + 3 * (1 - t) * t * t * self[2].y + t * t * t * self[3].y;
    return Point(x,y)

  def tOfPoint(self,p):
    precision = 1.0/50.0
    bestDist = float("inf")
    bestT = -1
    samples = self.regularSampleTValue(50)
    for t in samples:
      dist = self.pointAtTime(t).distanceFrom(p)
      if dist < bestDist:
        bestDist = dist
        bestT = t
    while precision > 1e-5:
      precision = precision / 2
      lower = bestT - precision
      if lower < 0: lower = 0
      upper = bestT + precision
      if upper > 1: upper = 1
      ldist = self.pointAtTime(lower).distanceFrom(p)
      rdist = self.pointAtTime(lower).distanceFrom(p)
      if ldist < bestDist:
        bestT = lower
        bestDist = ldist
      if rdist < bestDist:
        bestT = upper
        bestDist = rdist
    return bestT

  def splitAtTime(self,t):
    """Returns two segments, dividing the given segment at a point t (0->1) along the curve."""
    p4 = self[0].lerp(self[1],t)
    p5 = self[1].lerp(self[2],t)
    p6 = self[2].lerp(self[3],t)
    p7 = p4.lerp(p5,t)
    p8 = p5.lerp(p6,t)
    p9 = p7.lerp(p8,t)
    return (CubicBezier(self[0],p4,p7,p9), CubicBezier(p9,p8,p6,self[3]))

  def join(self,other):
    """Not currently implemented: join two `CubicBezier` together."""
    raise "Not implemented"

  def toQuadratic(self):
    """Not currently implemented: reduce this to a `QuadraticBezier`."""
    raise "Not implemented"

  def derivative(self):
    """Returns a `QuadraticBezier` representing the derivative of this curve."""
    return QuadraticBezier(
      (self[1]-self[0])*3,
      (self[2]-self[1])*3,
      (self[3]-self[2])*3
    )

  def flatten(self, degree=8):
    samples = self.regularSample(self.length/degree)
    ss = []
    for i in range(1,len(samples)):
      l = Line(samples[i-1], samples[i])
      l._orig = self
      ss.append(l)
    return ss

  def _findRoots(self,dimension):
    def cuberoot(v):
      if v<0: return -math.pow(-v,1/3.0)
      return math.pow(v,1/3.0)

    if dimension == "x":
      pa,pb,pc,pd = self[0].x,self[1].x,self[2].x,self[3].x
    elif dimension == "y":
      pa,pb,pc,pd = self[0].y,self[1].y,self[2].y,self[3].y
    else:
      raise SyntaxError("Meh.")

    a = (3*pa - 6*pb + 3*pc)
    b = (-3*pa + 3*pb)
    c = pa
    d = (-pa + 3*pb - 3*pc + pd)
    if d == 0: return []
    a = a/d
    b = b/d
    c = c/d
    p = (3*b - a*a)/3
    p3 = p/3
    q = (2*a*a*a - 9*a*b + 27*c)/27.0
    q2 = q/2
    discriminant = q2*q2 + p3*p3*p3
    if discriminant < 0:
      mp3  = -p/3
      mp33 = mp3*mp3*mp3
      r    = math.sqrt( mp33 )
      t    = -q / (2*r)
      cosphi = max(min(t,1),-1)
      phi  = math.acos(cosphi)
      crtr = cuberoot(r)
      t1   = 2*crtr
      root1 = t1 * math.cos(phi/3) - a/3
      root2 = t1 * math.cos((phi+2*math.pi)/3) - a/3
      root3 = t1 * math.cos((phi+4*math.pi)/3) - a/3
      roots = [root1, root2, root3]
      return sorted([x for x in roots if x >= 0 and x <= 1])

    if discriminant == 0:
      if q2 < 0:
        u1 = cuberoot(-q2)
      else:
        u1 =-cuberoot(q2);
      root1 = 2*u1 - a/3.0;
      root2 = -u1 - a/3.0;
      roots = [root1,root2]
      return sorted([x for x in roots if x >= 0 and x <= 1])

    sd = math.sqrt(discriminant);
    u1 = cuberoot(sd - q2);
    v1 = cuberoot(sd + q2);
    root1 = u1 - v1 - a/3;
    return [x for x in [root1] if x >= 0 and x <= 1]

  def _findDRoots(self):
    d = self.derivative()
    roots = []

    # We have f(t) = w1 (1-t)^2 + 2 w2 (1-t) t + w3 t^2
    # We want f(t) = a t^2 + b^t + c to solve with the quadratic formula
    roots.extend(quadraticRoots(d[0].x - 2*d[1].x + d[2].x, 2 * (d[1].x-d[0].x), d[0].x))
    roots.extend(quadraticRoots(d[0].y - 2*d[1].y + d[2].y, 2 * (d[1].y-d[0].y), d[0].y))
    return roots

  def findExtremes(self, inflections = False):
    """Returns a list of time `t` values for extremes of the curve."""
    r = self._findDRoots()
    if inflections:
      r.extend(self.derivative()._findDRoots())
    r.sort()
    return [ root for root in r if root >= 0.01 and root <= 0.99 ]

  def curvatureAtTime(self,t):
    """Returns the C curvature at time `t`.."""
    d = self.derivative()
    d2 = d.derivative()
    return d.pointAtTime(t).x * d2.pointAtTime(t).y - d.pointAtTime(t).y * d2.pointAtTime(t).x

  @property
  def tunniPoint(self):
    """Returns the Tunni point of this Bezier (the intersection of
    the handles)."""
    h1 = Line(self[0], self[1])
    h2 = Line(self[2], self[3])
    i = h1.intersections(h2, limited = False)
    if len(i)<1: return
    i = i[0].point
    if i.distanceFrom(self[0]) > 5 * self.length:
      return
    else:
      return i

  def balance(self):
    """Perform Tunni balancing on this Bezier."""
    p = self.tunniPoint
    if not p: return
    fraction1 = self[0].distanceFrom(self[1]) / self[0].distanceFrom(p)
    fraction2 = self[3].distanceFrom(self[2]) / self[3].distanceFrom(p)
    avg = (fraction2 + fraction1) / 2.0
    if avg > 0 and avg < 1:
      self[1] = self[0].lerp(p, avg)
      self[2] = self[3].lerp(p, avg)

  @property
  def hasLoop(self):
    a1 = self[0].x * (self[3].y - self[2].y) + self[0].y * (self[2].x - self[3].x) + self[3].x * self[2].y - self[3].y * self[2].x
    a2 = self[1].x * (self[0].y - self[3].y) + self[1].y * (self[3].x - self[0].x) + self[0].x * self[3].y - self[0].y * self[3].x
    a3 = self[2].x * (self[1].y - self[0].y) + self[2].y * (self[0].x - self[1].x) + self[1].x * self[0].y - self[1].y * self[0].x
    d3 = 3 * a3
    d2 = d3 - a2
    d1 = d2 - a2 + a1
    l = math.sqrt(d1 * d1 + d2 * d2 + d3 * d3)
    s = 0
    if l != 0: s = 1 / l
    d1 *= s
    d2 *= s
    d3 *= s
    d = 3 * d2 * d2 - 4 * d1 * d3
    if d >= 0: return False
    f1 = math.sqrt(-d)
    f2 = 2 * d1
    return ((d2 + f1) / f2, (d2 - f1) / f2)

  @property
  def area(self):
    """Returns the signed rea between the curve and the y-axis"""
    return (10 * (self[3].x*self[3].y - self[0].x*self[0].y) +
            6 * (self[1].x*self[0].y - self[0].x*self[1].y + self[3].x*self[2].y - self[2].x*self[3].y) +
            3 * (self[2].x*self[0].y - self[0].x*self[2].y + self[2].x*self[1].y - self[1].x*self[2].y +
                 self[3].x*self[1].y - self[1].x*self[3].y) +
                 self[3].x*self[0].y - self[0].x*self[3].y) / 20.
