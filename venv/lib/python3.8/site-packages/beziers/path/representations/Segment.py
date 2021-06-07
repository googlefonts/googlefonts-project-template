from beziers.path.representations.Nodelist import Node
from beziers.line import Line
from beziers.cubicbezier import CubicBezier
from beziers.quadraticbezier import QuadraticBezier
from beziers.point import Point
from beziers.utils import isclose

class SegmentRepresentation(object):
  def __init__(self, path, segments=[]):
    self.path = path
    from beziers.path import BezierPath
    assert isinstance(path, BezierPath)
    self.segments = []
    if segments:
      self.segments = segments

  def data(self):
    return self.segments

  def toNodelist(self):
    first = self.segments[0][0]
    nodelist=[]
    if len(self.segments[0]) == 2:
      nodelist.append(Node(first.x, first.y, "line"))
    else:
      nodelist.append(Node(first.x, first.y, "curve"))
    for seg in self.segments:
      if len(seg) == 4:
        nodelist.append(Node(seg[1].x, seg[1].y, "offcurve"))
        nodelist.append(Node(seg[2].x, seg[2].y, "offcurve"))
        nodelist.append(Node(seg[3].x, seg[3].y, "curve"))
      elif len(seg) == 3:
        nodelist.append(Node(seg[1].x, seg[1].y, "offcurve"))
        nodelist.append(Node(seg[2].x, seg[2].y, "curve"))
      else:
        nodelist.append(Node(seg[1].x, seg[1].y, "line"))
    return nodelist

  def appendSegment(self, seg):
    seg = [Point(n[0],n[1]) for n in seg]
    if len(seg) == 2:
      self.segments.append(Line(*seg))
    elif len(seg) == 3:
      self.segments.append(QuadraticBezier(*seg))
    elif len(seg) == 4:
      self.segments.append(CubicBezier(*seg))
    else:
      raise ValueError("Unknown segment type")

  @classmethod
  def fromNodelist(cls, path, nodelist):
    self = SegmentRepresentation(path)
    # Find first oncurve
    firstOncurve = -1
    for ix, n in enumerate(nodelist):
      if n.type != "offcurve":
        firstOncurve = ix
        break
    first = nodelist[firstOncurve]
    seg = [(first.x,first.y)]

    for n in nodelist[firstOncurve+1:]:
      if n.type == "offcurve":
        seg.append((n.x,n.y))
      if n.type == "line" or n.type == "curve":
        seg.append((n.x,n.y))
        self.appendSegment(seg)
        seg = [(n.x,n.y)]
    for n in nodelist[:firstOncurve]:
      if n.type == "offcurve":
        seg.append((n.x,n.y))
      if n.type == "line" or n.type == "curve":
        seg.append((n.x,n.y))
        self.appendSegment(seg)
        seg = [(n.x,n.y)]

    # Closed?
    if self.path.closed:
      if len(seg) == 1 and isclose(seg[-1][0], first.x) and isclose(seg[-1][1], first.y):
        pass
      else:
        seg.append((first.x,first.y))
        self.appendSegment(seg)
    return self
