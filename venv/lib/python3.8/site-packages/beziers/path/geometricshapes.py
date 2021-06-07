from beziers.point import Point
from beziers.path import BezierPath
from beziers.cubicbezier import CubicBezier
from beziers.line import Line
import math

CIRCULAR_SUPERNESS = 4./3.*(math.sqrt(2)-1)

west  = Point(-1,0)
east  = Point(1,0)
north = Point(0,1)
south = Point(0,-1)

def Circle(x_radius, origin=None, superness=CIRCULAR_SUPERNESS):
  """Returns a path representing a circle of given radius. You can specify the
  `origin` as a Point and the `superness` of the circle."""
  return Ellipse(x_radius, x_radius, origin=origin, superness=superness)

def Ellipse(x_radius, y_radius, origin=None, superness=CIRCULAR_SUPERNESS):
  """Returns a path representing an ellipse of given x and y radii.
  You can specify the `origin` as a Point and the `superness` of the ellipse."""
  if not origin:
    origin = Point(0,0)
  w = origin + west * x_radius
  e = origin + east * x_radius
  n = origin + north * y_radius
  s = origin + south * y_radius

  w_n = CubicBezier(w,
                    w + north * y_radius * superness,
                    n + west * x_radius * superness,
                    n)
  n_e = CubicBezier(n,
                    n + east * x_radius * superness,
                    e + north * y_radius * superness,
                    e)
  e_s = CubicBezier(e,
                  e + south * y_radius * superness,
                  s + east * x_radius * superness,
                  s)
  s_w = CubicBezier(s,
                  s + west * x_radius * superness,
                  w + south * y_radius * superness,
                  w)
  return BezierPath.fromSegments([w_n, n_e, e_s, s_w])

def Rectangle(width, height, origin=None):
  """Returns a path representing an rectangle of given width and height.
  You can specify the `origin` as a Point."""
  if not origin:
    origin = Point(0,0)
  tl = origin + west * width / 2.0 + north * height / 2.0
  tr = origin + east * width / 2.0 + north * height / 2.0
  bl = origin + west * width / 2.0 + south * height / 2.0
  br = origin + east * width / 2.0 + south * height / 2.0

  return BezierPath.fromSegments([
    Line(tl,tr), Line(tr,br), Line(br,bl), Line(bl,tl)
  ])

def Square(width, origin=None):
  """Returns a path representing a square of given width.
  You can specify the `origin` as a Point."""
  return Rectangle(width, width, origin=origin)
