import unittest
from beziers.cubicbezier import CubicBezier
from beziers.line import Line
from beziers.point import Point
from beziers.path import BezierPath
from beziers.path.representations.Segment import SegmentRepresentation

class IntersectionMethods(unittest.TestCase):

  def test_line_line(self):
    l1 = Line(Point(310,389), Point(453,222))
    l2 = Line(Point(289,251), Point(447,367))
    # Sanity check
    self.assertEqual(len(l1.intersections(l2)),1)

  def test_cubic_line(self):
    q = CubicBezier(
      Point(100,240), Point(30,60), Point(210,230), Point(160,30))
    l = Line(Point(25,260), Point(230,20))
    path = BezierPath()
    path.closed = False
    path.activeRepresentation = SegmentRepresentation(path,[q])
    i = q.intersections(l)
    self.assertEqual(len(i),3)
    self.assertEqual(i[0].point,q.pointAtTime(0.117517031451))
    self.assertEqual(i[1].point,q.pointAtTime(0.518591792307))
    self.assertEqual(i[2].point,q.pointAtTime(0.867886610031))
    # print q.intersections(l)
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # path.plot(ax)

    # path = BezierPath()
    # path.closed = False
    # path.activeRepresentation = SegmentRepresentation(path,[l])
    # path.plot(ax)

    # for n in q.intersections(l):
    #   circle = plt.Circle((n.point.x, n.point.y), 1, fill=False)
    #   ax.add_artist(circle)

    # plt.show()

  def test_cubic_cubic(self):
    # q1 = Bezier(10,100, 90,30, 40,140, 220,220)
    # q2 = Bezier(5,150, 180,20, 80,250, 210,190)
    # console.log(q1.intersects(q2))
    q1 = CubicBezier(
        Point(10,100), Point(90,30), Point(40,140), Point(220,220)
    )
    q2 = CubicBezier(
        Point(5,150), Point(180,20), Point(80,250), Point(210,190)
    )
    i = q1.intersections(q2)
    # self.assertEqual(len(i),3)
    # self.assertAlmostEqual(i[0].point.x,81.7904225873)
    # self.assertAlmostEqual(i[0].point.y,109.899396337)
    # self.assertAlmostEqual(i[1].point.x,133.186831292)
    # self.assertAlmostEqual(i[1].point.y,167.148173322)
    # self.assertAlmostEqual(i[2].point.x,179.869157678)
    # self.assertAlmostEqual(i[2].point.y,199.661989162)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    path = BezierPath()
    path.closed = False
    path.activeRepresentation = SegmentRepresentation(path,[q1])
    path.plot(ax)
    path.activeRepresentation = SegmentRepresentation(path,[q2])
    path.plot(ax)

    for n in i:
      circle = plt.Circle((n.point.x, n.point.y), 2, fill=True, color="red")
      ax.add_artist(circle)

    # plt.show()

  def test_cubic_line_2(self):
    s1 = CubicBezier.fromRepr("B<<584.0,126.03783241124995>-<402.0,163.0378324112499>-<220.00000000000003,200.03783241124995>-<38.0,237.03783241124995>>"),
    ray = Line.fromRepr("L<<357.4,-9.99999999999999>--<357.6,250.2692949284206>>")
    assert (s1[0].intersections(ray))

  def test_cubic_line_3(self):
    seg = CubicBezier.fromRepr("B<<320.0,454.0>-<277.0,454.0>-<230.0,439.0>-<189.0,417.0>>")
    ray = Line.fromRepr("L<<254.5,221.5>--<254.5000000000001,887.6681469418963>>")
    assert seg.intersections(ray)
