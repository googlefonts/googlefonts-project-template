from beziers.point import Point

class Node(object):
  def __init__(self, x,y,type):
    self.point = Point(x,y)
    self.type = type

  @property
  def x(self):
    return self.point.x

  @property
  def y(self):
    return self.point.y

  def __repr__(self):
    return "<x=%s y=%s %s>" % (self.x,self.y,self.type)

class NodelistRepresentation(object):
  def __init__(self, path, nl = None):
    self.path = path
    from beziers.path import BezierPath
    assert isinstance(path, BezierPath)
    self.nodes = []
    if nl:
      self.nodes = nl

  def data(self):
    return self.nodes

  def toNodelist(self):
    return self.nodes

  def fromNodelist(self):
    return self
