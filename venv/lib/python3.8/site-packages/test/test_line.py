import unittest
from beziers.line import Line
from beziers.point import Point

class LineMethods(unittest.TestCase):
  def test_slope(self):
    l = Line(Point(0,10),Point(20,20.4))
    self.assertAlmostEqual(l.slope, 0.52)

  def test_intercept(self):
    l = Line(Point(0,10),Point(20,20.4))
    self.assertAlmostEqual(l.intercept, 10)

