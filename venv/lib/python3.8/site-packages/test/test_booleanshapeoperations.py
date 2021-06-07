import unittest
from beziers.path import BezierPath
from beziers.path.representations.Nodelist import NodelistRepresentation, Node
from beziers.point import Point
from beziers.path.geometricshapes import Circle, Square

class BooleanShapeOperations(unittest.TestCase):
  def drawIt(self, s,c,paths):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    s.plot(ax,drawNodes=False)
    c.plot(ax)
    for p in paths:
      p.plot(ax,drawNodes=False,color="red")
    plt.show()

  def not_a_test_square_circle_union(self):
    subject = Square(10, origin=Point(5,5))
    clip = Circle(10, origin=Point(15,15))
    paths = subject.union(clip)
    self.drawIt(subject,clip,paths)