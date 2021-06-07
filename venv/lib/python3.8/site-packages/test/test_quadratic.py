import unittest
from beziers.quadraticbezier import QuadraticBezier
from beziers.point import Point

class QuadraticMethods(unittest.TestCase):
  def test_split(self):
    # console.log((new Bezier(150,40,80,30,105,150)).split(0.2))
    q = QuadraticBezier(
      Point(150,40), Point(80,30), Point(105,150))
    left, right = q.splitAtTime(0.2)
    self.assertEqual(left[1],Point(136,38))
    self.assertEqual(right[1],Point(85,54))

  def test_extremes(self):
    q = QuadraticBezier(
      Point(70,250), Point(13,187), Point(209,58))
    r = q.findExtremes()
    self.assertEqual(len(r), 1)
    self.assertAlmostEqual(r[0], 0.22529644268774704)

  def test_extremes2(self):
    # console.log((new Bezier(127,242,71,150,210,60)).extrema())
    q = QuadraticBezier(
      Point(127,242), Point(71,150), Point(210,60))
    r = q.findExtremes()
    self.assertEqual(len(r), 1)
    self.assertAlmostEqual(r[0], 0.28717948717948716)

  def test_extremes3(self):
    # console.log((new Bezier(127,242,27,5,210,60)).extrema())
    q = QuadraticBezier(
      Point(127,242), Point(27,5), Point(210,60))
    r = q.findExtremes()
    self.assertEqual(len(r), 2)
    self.assertAlmostEqual(r[0], 0.35335689045936397)
    self.assertAlmostEqual(r[1], 0.8116438356164384)
    # from beziers.path import BezierPath
    # import matplotlib.pyplot as plt
    # path = BezierPath.fromSegments([q])
    # fig, ax = plt.subplots()
    # path.closed = False
    # path.addExtremes()
    # path.plot(ax)
    # plt.show()


  def test_extremes4(self):
    q = QuadraticBezier(
      Point(664,1075),
      Point(732,1167),
      Point(800,1239)
    )
    r = q.findExtremes()
    self.assertEqual(len(r), 0)

