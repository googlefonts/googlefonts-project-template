import unittest
from beziers.quadraticbezier import QuadraticBezier
from beziers.cubicbezier import CubicBezier
from beziers.point import Point

class ArcLengthMethods(unittest.TestCase):
  def test_quadraticLength(self):
    b1 = QuadraticBezier(
      Point(150,40),
      Point(80,30),
      Point(105,150)
    )
    self.assertAlmostEqual(b1.length, 144.79561403359523)

    b2 = QuadraticBezier(
      Point(707,596),
      Point(645,596),
      Point(592,623)
    )
    self.assertAlmostEqual(b2.length, 119.25113694489232)

  def test_cubicLength(self):
    b1 = CubicBezier(
        Point(100,25),
        Point(10,90),
        Point(110,100),
        Point(132,192)
      )
    self.assertAlmostEqual(b1.length, 202.20118972656385)
