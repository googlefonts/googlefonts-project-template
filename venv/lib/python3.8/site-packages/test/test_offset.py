
import unittest
from beziers.path.representations.GSPath import GSPathRepresentation
from beziers.path.representations.Segment import SegmentRepresentation
from beziers.path.representations.Nodelist import Node
from beziers.point import Point
from beziers.cubicbezier import CubicBezier
from beziers.line import Line
from beziers.path import BezierPath
from dotmap import DotMap

class PathTests(unittest.TestCase):
  def not_a_test_offset(self):
    b = DotMap({ "closed": False,
    "nodes": [
     {"x": 412.0, "y":500.0, "type":"line"},
     {"x": 308.0, "y":665.0, "type":"offcurve"},
     {"x": 163.0, "y":589.0, "type":"offcurve"},
     {"x": 163.0, "y":504.0, "type":"curve"},
     {"x": 163.0, "y":424.0, "type":"offcurve"},
     {"x": 364.0, "y":321.0, "type":"offcurve"},
     {"x": 366.0, "y":216.0, "type":"curve"},
     {"x": 368.0, "y":94.0, "type":"offcurve"},
     {"x": 260.0, "y":54.0, "type":"offcurve"},
     {"x": 124.0, "y":54.0, "type":"curve"}
    ]})
    path = BezierPath()
    path.activeRepresentation = GSPathRepresentation(path,b)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    path.addExtremes()
    path.plot(ax)
    for n in path.asSegments():
      p = n.tunniPoint
      if p:
        circle = plt.Circle((p.x, p.y), 1, fill=False, color="blue")
        ax.add_artist(circle)
      n.balance()
    path.translate(Point(5,5))
    path.plot(ax, color="red")
    # o1 = path.offset(Point(10,10))
    # o2 = path.offset(Point(-10,-10))
    # o2.reverse()
    # o1.append(o2)
    # o1.plot(ax)
    plt.show()