import unittest
from beziers.path.representations.GSPath import GSPathRepresentation
from beziers.path.representations.Segment import SegmentRepresentation
from beziers.path.representations.Nodelist import Node
from beziers.point import Point
from beziers.cubicbezier import CubicBezier
from beziers.line import Line
from beziers.path import BezierPath
from dotmap import DotMap
from beziers.path.geometricshapes import Rectangle


class PathTests(unittest.TestCase):
  # def test_representations(self):
  #   b = DotMap({ "closed": True,
  #   "nodes": [
  #   {"x":385.0, "y":20.0, "type":"offcurve"},
  #   { "x":526.0, "y":79.0, "type":"offcurve"},
  #   { "x":566.0, "y":135.0, "type":"curve"},
  #   { "x":585.0, "y":162.0, "type":"offcurve"},
  #   { "x":566.0, "y":260.0, "type":"offcurve"},
  #   { "x":484.0, "y":281.0, "type":"curve"},
  #   { "x":484.0, "y":407.0, "type":"offcurve"},
  #   { "x":381.0, "y":510.0, "type":"offcurve"},
  #   { "x":255.0, "y":510.0, "type":"curve"},
  #   { "x":26.0, "y":281.0, "type":"line"},
  #   { "x":26.0, "y":155.0, "type":"offcurve"},
  #   { "x":129.0, "y":20.0, "type":"offcurve"},
  #   { "x":255.0, "y":20.0, "type":"curve"}
  #   ]})
  #   path = BezierPath()
  #   path.activeRepresentation = GSPathRepresentation(path,b)
  #   nl = path.asNodelist()
  #   self.assertEqual(len(nl), 13)
  #   self.assertIsInstance(nl[1], Node)
  #   self.assertEqual(nl[1].type,"offcurve")
  #   self.assertAlmostEqual(nl[1].x,526.0)

  #   segs = path.asSegments()
  #   self.assertEqual(len(segs), 5)
  #   self.assertIsInstance(segs[1], CubicBezier)
  #   self.assertIsInstance(segs[2], Line)

  def test_addextremes(self):
    q = CubicBezier(
      Point(42,135), Point(129,242), Point(167,77), Point(65,59)
    )
    ex = q.findExtremes()
    self.assertEqual(len(ex),2)
    path = BezierPath()
    path.closed = False
    path.activeRepresentation = SegmentRepresentation(path,[q])
    path.addExtremes()
    path.balance()
    segs = path.asSegments()
    self.assertEqual(len(segs), 3)
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # path.plot(ax)
    # plt.show()

  def test_overlap(self):
    nodes = [ Node(698.0,413.0,"offcurve"),
      Node(401.0,179.0,"offcurve"),
      Node(401.0,274.0,"curve"),
      Node(401.0,368.0,"offcurve"),
      Node(315.0,445.0,"offcurve"),
      Node(210.0,445.0,"curve"),
      Node(104.0,445.0,"offcurve"),
      Node(18.0,368.0,"offcurve"),
      Node(18.0,274.0,"curve"),
      Node(18.0,179.0,"offcurve"),
      Node(439.0,400.0,"offcurve"),
      Node(533.0,405.0,"curve")
    ]
    p = BezierPath.fromNodelist(nodes)
    p.closed = True
    i = p.getSelfIntersections()
    self.assertEqual(len(i),1)
    self.assertAlmostEqual(i[0].point.x, 377.71521068)

    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # p.plot(ax)
    # for n in i:
    #   circle = plt.Circle((n.point.x, n.point.y), 2, fill=True, color="red")
    #   ax.add_artist(circle)
    # plt.show()

    p = BezierPath.fromNodelist([
      Node(310.0,389.0,"line"),
      Node(453.0,222.0,"line"),
      Node(289.0,251.0,"line"),
      Node(447.0,367.0,"line"),
      Node(578.0,222.0,"line"),
      Node(210.0,-8.0,"line"),
    ])

    i = p.getSelfIntersections()
    self.assertEqual(len(i),1)
    self.assertEqual(i[0].point,Point(374.448829525,313.734583702))

  def test_splitatpoints(self):
    p = BezierPath.fromNodelist([
      Node(297.0,86.0,"offcurve"),
      Node(344.0,138.0,"offcurve"),
      Node(344.0,203.0,"curve"),
      Node(344.0,267.0,"offcurve"),
      Node(297.0,319.0,"offcurve"),
      Node(240.0,319.0,"curve"),
      Node(183.0,319.0,"offcurve"),
      Node(136.0,267.0,"offcurve"),
      Node(136.0,203.0,"curve"),
      Node(136.0,138.0,"offcurve"),
      Node(183.0,86.0,"offcurve"),
      Node(240.0,86.0,"curve"),
    ])
    splitlist = []
    for seg in p.asSegments():
      for t in seg.regularSampleTValue(5):
        splitlist.append((seg,t))
    p.splitAtPoints(splitlist)
    self.assertEqual(len(p.asSegments()),24)

  def test_inside(self):
    p = BezierPath.fromNodelist([
      Node(329,320,"line"),
      Node(564,190,"line"),
      Node(622,332,"offcurve"),
      Node(495,471,"offcurve"),
      Node(329,471,"curve"),
      Node(164,471,"offcurve"),
      Node(34,334,"offcurve"),
      Node(93,190,"curve")
    ])
    self.assertTrue(p.pointIsInside(Point(326,423)))
    self.assertFalse(p.pointIsInside(Point(326,123)))
    self.assertFalse(p.pointIsInside(Point(326,251)))
    self.assertTrue(p.pointIsInside(Point(526,251)))
    self.assertTrue(p.pointIsInside(Point(126,251)))

  def test_area(self):
    p = Rectangle(200, 100)
    self.assertEqual(p.area, 200 * 100)
    self.assertEqual(p.signed_area, -200 * 100)
    self.assertEqual(p.direction, -1)
    p.reverse()
    self.assertEqual(p.signed_area, 200 * 100)
    self.assertEqual(p.direction, 1)

