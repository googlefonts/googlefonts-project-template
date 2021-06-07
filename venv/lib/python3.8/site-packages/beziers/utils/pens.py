from fontTools.pens.basePen import BasePen
from beziers.path.representations.Nodelist import NodelistRepresentation, Node
from beziers.path import BezierPath


class BezierPathCreatingPen(BasePen):
  def __init__(self, *args, **kwargs):
    super(BezierPathCreatingPen, self).__init__(*args, **kwargs)
    self.paths = []
    self.path = BezierPath()
    self.nodeList = []
  def _moveTo(self, p):
    self.nodeList = [Node(p[0], p[1], "move")]
  def _lineTo(self, p):
    self.nodeList.append(Node(p[0], p[1], "line"))
  def _curveToOne(self, p1, p2, p3):
    self.nodeList.append(Node(p1[0], p1[1], "offcurve"))
    self.nodeList.append(Node(p2[0], p2[1], "offcurve"))
    self.nodeList.append(Node(p3[0], p3[1], "curve"))
  def _qCurveToOne(self, p1, p2):
    self.nodeList.append(Node(p1[0], p1[1], "offcurve"))
    self.nodeList.append(Node(p2[0], p2[1], "curve"))
  def _closePath(self):
    self.path.closed = True
    self.path.activeRepresentation = NodelistRepresentation(self.path, self.nodeList)
    self.paths.append(self.path)
    self.path = BezierPath()
