from beziers.point import Point
from beziers.affinetransformation import AffineTransformation
from beziers.utils.samplemixin import SampleMixin
from beziers.utils.intersectionsmixin import IntersectionsMixin
from beziers.boundingbox import BoundingBox

class Segment(IntersectionsMixin,SampleMixin,object):

  """A segment is part of a path. Although this package is called
  `beziers.py`, it's really for font people, and paths in the font
  world are made up of cubic Bezier curves, lines and (if you're
  dealing with TrueType) quadratic Bezier curves. Each of these
  things is represented as an object derived from the Segment base
  class. So, when you inspect the path in the segment representation,
  you will get a list of CubicBezier, Line and QuadraticBezier objects,
  all of which derive from Segment.

  Because of this, a Segment can have two, three or four elements:
  lines have two end points; quadratic Beziers have a start, a control
  point and an end point; cubic have a start, two control points and
  an end point.

  You can pretend that a Segment object is an array and index it like
  one::

      q = CubicBezier(
        Point(122,102), Point(35,200), Point(228,145), Point(190,46)
      )

      start, cp1, cp2, end = q[0],q[1],q[2],q[3]

  You can also access the start and end points like so::

      start = q.start
      end = q.end

  """

  def __getitem__(self, item):
    return self.points[item]
  def __setitem__(self, key, item):
      self.points[key] = item
  def __len__(self):
    return len(self.points)
  def __eq__(self,other):
    if self.order != other.order: return False
    for p in range(0,self.order):
      if self[p] != other[p]: return False
    return True
  def __hash__(self):
    return hash(tuple(self.points))
  def __ne__(self,other):
    return not self.__eq__(other)

  def clone(self):
    """Returns a new Segment which is a copy of this segment."""
    klass = self.__class__
    return klass(*[ p.clone() for p in self.points ])

  def round(self):
    """Rounds the points of segment to integer coordinates."""
    self.points = [ p.rounded() for p in self.points ]

  @property
  def order(self):
    return len(self.points)

  @property
  def start(self):
    """Returns a Point object representing the start of this segment."""
    return self.points[0]

  @property
  def end(self):
    """Returns a Point object representing the end of this segment."""
    return self.points[-1]

  @property
  def startAngle(self):
    return (self.points[1]-self.points[0]).angle

  @property
  def endAngle(self):
    return (self.points[-1]-self.points[-2]).angle

  def tangentAtTime(self,t):
    """Returns a `Point` representing the unit vector of tangent at time `t`."""
    return self.derivative().pointAtTime(t).toUnitVector()

  def normalAtTime(self,t):
    """Returns a `Point` representing the normal (rotated tangent) at time `t`."""
    tan = self.tangentAtTime(t)
    return Point(-tan.y,tan.x)

  def translated(self,vector):
    """Returns a *new Segment object* representing the translation of
    this segment by the given vector. i.e.::

      >>> l = Line(Point(0,0), Point(10,10))
      >>> l.translated(Point(5,5))
      L<<5.0,5.0>--<15.0,15.0>>
      >>> l
      L<<0.0,0.0>--<10.0,10.0>>

    """

    klass = self.__class__
    return klass(*[ p+vector for p in self.points ])

  def rotated(self,around, by):
    """Returns a *new Segment object* representing the rotation of
    this segment around the given point and by the given angle. i.e.::

      >>> l = Line(Point(0,0), Point(10,10))
      >>> l.rotated(Point(5,5), math.pi/2)
      L<<10.0,-8.881784197e-16>--<-8.881784197e-16,10.0>>

    """

    klass = self.__class__
    pNew = [ p.clone() for p in self.points]
    for p in pNew: p.rotate(around,by)
    return klass(*pNew)

  def scaled(self,bx):
    """Returns a *new Segment object* representing the scaling of
    this segment by the given magnification. i.e.::

      >>> l = Line(Point(0,0), Point(10,10))
      >>> l.scaled(2)
      L<<0,0>--<20,20>>

    """

    klass = self.__class__
    pNew = [ p * bx for p in self.points]
    return klass(*pNew)

  def transformed(self, transformation):
    """Returns a *new Segment object* transformed by the given AffineTransformation matrix."""
    klass = self.__class__
    pNew = [ p.clone() for p in self.points]
    for p in pNew: p.transform(transformation)
    return klass(*pNew)

  def alignmentTransformation(self):
    m = AffineTransformation.translation(self.start * -1)
    m.rotate((self.end.transformed(m)).angle * -1)
    return m

  def aligned(self):
    """Returns a *new Segment object* aligned to the origin. i.e.
    with the first point translated to the origin (0,0) and the
    last point with y=0. Obviously, for a `Line` this is a bit pointless,
    but it's quite handy for higher-order curves."""
    return self.transformed(self.alignmentTransformation())

  def lengthAtTime(self, t):
    """Returns the length of the subset of the path from the start
    up to the point t (0->1), where 1 is the end of the whole curve."""
    s1,_ = self.splitAtTime(t)
    return s1.length

  def reversed(self):
    """Returns a new segment with the points reversed."""
    klass = self.__class__
    return klass(*list(reversed(self.points)))

  def bounds(self):
    """Returns a BoundingBox object for this segment."""
    bounds = BoundingBox()
    ex = self.findExtremes()
    ex.append(0)
    ex.append(1)
    for t in ex:
      bounds.extend(self.pointAtTime(t))
    return bounds

  @property
  def hasLoop(self):
    """Returns True if the segment has a loop. (Only possible for cubics.)"""
    return False
  
