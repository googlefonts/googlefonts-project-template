import unittest
from beziers.cubicbezier import CubicBezier
from beziers.point import Point
from beziers.path import BezierPath

class CubicMethods(unittest.TestCase):
  def test_extremes(self):
    q = CubicBezier(
      Point(65,59), Point(194,90), Point(220,260), Point(70,261)
    )
    # console.log(Bezier(65,59, 194,90, 220,260, 70,261).extrema())
    r = q.findExtremes()
    self.assertEqual(len(r), 1)
    self.assertAlmostEqual(r[0], 0.5275787707261016)
    r = q.findExtremes(inflections = True)
    self.assertEqual(len(r), 2)
    self.assertAlmostEqual(r[0], 0.4512987012987013)
    self.assertAlmostEqual(r[1], 0.5275787707261016)


  def test_length(self):
    q = CubicBezier(
      Point(120,160), Point(35,200), Point(220,260), Point(220,40)
    )
    self.assertAlmostEqual(q.length,272.87003168)

  def test_align(self):
    q = CubicBezier(
      Point(120,160), Point(35,200), Point(220,260), Point(220,40)
    )
    s = q.aligned()
    self.assertAlmostEqual(s[0].x,0.0)
    self.assertAlmostEqual(s[0].y,0.0)
    self.assertAlmostEqual(s[1].x,-85.14452515537582)
    self.assertAlmostEqual(s[1].y,-39.69143277919774)
    self.assertAlmostEqual(s[2].x,-12.803687993289572)
    self.assertAlmostEqual(s[2].y,140.84056792618557)
    self.assertAlmostEqual(s[3].x,156.2049935181331)
    self.assertAlmostEqual(s[3].y,0.0)

  def test_curvature(self):
    q = CubicBezier(
      Point(122,102), Point(35,200), Point(228,145), Point(190,46)
    )
    self.assertAlmostEqual(q.curvatureAtTime(0.5),-103450.5)

  def test_loop(self):
    q = CubicBezier(
      Point(171,272), Point(388,249), Point(167,444), Point(388,176)
    )
    self.assertTrue(not q.hasLoop)

    q = CubicBezier(
      Point(171,272), Point(595,249), Point(167,444), Point(388,176)
    )
    roots = q.hasLoop
    p1 = q.pointAtTime(roots[0])
    p2 = q.pointAtTime(roots[1])
    self.assertTrue(q.hasLoop)
    self.assertEqual(p1,p2)