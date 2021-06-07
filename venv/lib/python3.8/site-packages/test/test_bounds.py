import unittest
from beziers.quadraticbezier import QuadraticBezier
from beziers.point import Point
from beziers.boundingbox import BoundingBox

class BBoxMethods(unittest.TestCase):
  def test_overlap(self):
    b1 = BoundingBox()
    b2 = BoundingBox()
    b1.extend(Point(5,5))
    b1.extend(Point(10,10))
    b2.extend(Point(7,7))
    b2.extend(Point(14,14))
    print("%s v %s" % (b1,b2))
    self.assertTrue(b1.overlaps(b2))
    self.assertTrue(b2.overlaps(b1))

  def test_quadratic_bounds(self):
    # console.log((new Bezier(150,40,80,30,105,150)).bbox())
    q = QuadraticBezier(
      Point(150,40), Point(80,30), Point(105,150))
    b = q.bounds()
    self.assertAlmostEqual(b.bl.x,98.42105263157895)
    self.assertAlmostEqual(b.tr.x,150)
    self.assertAlmostEqual(b.bl.y,39.23076923076923)
    self.assertAlmostEqual(b.tr.y,150)
