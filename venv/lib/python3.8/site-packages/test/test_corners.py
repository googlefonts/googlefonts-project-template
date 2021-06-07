import unittest
from beziers.utils.curvefitter import CurveFit
from beziers.path import BezierPath
from beziers.point import Point
from beziers.path.representations.Nodelist import NodelistRepresentation, Node

class CornerMethods(unittest.TestCase):
  def test_corners(self):
    nl = [
      Node(302.0,492.0,"line"),
      Node(176.0,432.0,"line"),
      Node(-51.0,325.0,"offcurve"),
      Node(-74.0,484.0,"offcurve"),
      Node(73.0,570.0,"curve"),
      Node(85.0,764.0,"offcurve"),
      Node(290.0,748.0,"offcurve"),
      Node(418.0,688.0,"curve"),
    ]
    path = BezierPath.fromNodelist(nl)
    path.closed = False
    for seg1, seg2 in path.segpairs():
      print(seg1.endAngle * 57.2958, seg2.startAngle * 57.2958)
