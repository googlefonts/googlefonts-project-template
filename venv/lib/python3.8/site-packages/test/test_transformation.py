import unittest
from beziers.point import Point
from beziers.cubicbezier import CubicBezier
from beziers.affinetransformation import AffineTransformation
import math

class AffineTransformationMethods(unittest.TestCase):
  def test_translate(self):
    p = Point(30,70)
    p.rotate(Point(0,0), math.pi/4)
    self.assertEqual(p.x, -28.284271247461906)
    self.assertEqual(p.y, 70.71067811865476)

    p = Point(30,70)
    m = AffineTransformation.rotation(math.pi/4)
    p.transform(m)
    self.assertAlmostEqual(p.x, -28.284271247461906)
    self.assertAlmostEqual(p.y, 70.71067811865476)

    p = Point(0,10)
    m = AffineTransformation.translation(Point(5,-2))
    p.transform(m)
    self.assertEqual(p.x, 5)
    self.assertEqual(p.y, 8)

  def test_scale(self):
    p = Point(4,5)
    m = AffineTransformation.scaling(2)
    p.transform(m)
    self.assertEqual(p.x, 8)
    self.assertEqual(p.y, 10)

    p = Point(4,5)
    m = AffineTransformation.scaling(1.5, -2)
    p.transform(m)
    self.assertEqual(p.x, 6)
    self.assertEqual(p.y, -10)

  def test_multiple_application(self):
    p = Point(10,10)
    m = AffineTransformation()
    m.translate(Point(6,5))
    m.scale(1.5,2)
    p.transform(m)
    self.assertEqual(p.x, 24)
    self.assertEqual(p.y, 30)
