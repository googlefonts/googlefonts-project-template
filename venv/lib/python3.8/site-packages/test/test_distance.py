import unittest
from beziers.path.geometricshapes import Circle
from beziers.point import Point
from beziers.path import BezierPath


def drawIt(s, c, segs):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    s.plot(ax, drawNodes=False)
    c.plot(ax)
    for s in segs:
        BezierPath.fromSegments([s]).plot(ax, drawNodes=False, color="red")
    plt.show()


class DistanceMethods(unittest.TestCase):
    def test_distance(self):
        p1 = Circle(50)
        p2 = Circle(50, origin=Point(200, 0))
        d = p1.distanceToPath(p2)
        # drawIt(p1, p2, [d[3], d[4]])
        self.assertAlmostEqual(d[0], 100)

    def test_distance2(self):
        p1 = Circle(50)
        p2 = Circle(50, origin=Point(100, 100))
        d = p1.distanceToPath(p2)
        # drawIt(p1, p2, [d[3], d[4]])
        self.assertAlmostEqual(d[0], 41.4531774254)
