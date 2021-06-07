from beziers.path.representations.Segment import SegmentRepresentation
from beziers.path.representations.Nodelist import NodelistRepresentation, Node
from beziers.point import Point
from beziers.boundingbox import BoundingBox
from beziers.utils.samplemixin import SampleMixin
from beziers.utils.booleanoperationsmixin import BooleanOperationsMixin
from beziers.segment import Segment
from beziers.line import Line
from beziers.cubicbezier import CubicBezier

import math

if not hasattr(math, "isclose"):
  def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
  math.isclose = isclose

class BezierPath(BooleanOperationsMixin,SampleMixin,object):
  """`BezierPath` represents a collection of `Segment` objects - the
  curves and lines that make up a path.

  One of the really fiddly things about manipulating Bezier paths in
  a computer is that there are various ways to represent them.
  Different applications prefer different representations. For instance,
  when you're drawing a path on a canvas, you often want a list of nodes
  like so::

    { "x":255.0, "y":20.0, "type":"curve"},
    { "x":385.0, "y":20.0, "type":"offcurve"},
    { "x":526.0, "y":79.0, "type":"offcurve"},
    { "x":566.0, "y":135.0, "type":"curve"},
    { "x":585.0, "y":162.0, "type":"offcurve"},
    { "x":566.0, "y":260.0, "type":"offcurve"},
    { "x":484.0, "y":281.0, "type":"curve"},
    ...

  But when you're doing Clever Bezier Mathematics, you generally want
  a list of segments instead::

    [ (255.0,20.0), (385.0,20.0), (526.0,79.0), (566.0,135.0)],
    [ (566.0,135.0), (585.0,162.0), (566.0,260.0), (484.0,281.0)],

  The Beziers module is designed to allow you to move fluidly between these
  different representations depending on what you're wanting to do.

  """

  def __init__(self):
    self.activeRepresentation = None
    self.closed = True


  @classmethod
  def fromPoints(self, points, error = 50.0, cornerTolerance = 20.0, maxSegments = 20):
    """Fit a poly-bezier curve to the points given. This operation should be familiar
    from 'pencil' tools in a vector drawing application: the application samples points
    where your mouse pointer has been dragged, and then turns the sketch into a Bezier
    path. The goodness of fit can be controlled by tuning the `error` parameter. Corner
    detection can be controlled with `cornerTolerance`.

    Here are some points fit with `error=100.0`:

..  figure:: curvefit1.png
    :scale: 75 %
    :alt: curvefit1


    And with `error=10.0`:

..  figure:: curvefit2.png
    :scale: 75 %
    :alt: curvefit1

    """
    from beziers.utils.curvefitter import CurveFit
    segs = CurveFit.fitCurve(points, error, cornerTolerance, maxSegments)
    path = BezierPath()
    path.closed = False
    path.activeRepresentation = SegmentRepresentation(path,segs)
    return path

  @classmethod
  def fromSegments(klass, array):
    """Construct a path from an array of Segment objects."""
    self = klass()
    for a in array: assert(isinstance(a, Segment))
    self.activeRepresentation = SegmentRepresentation(self,array)
    return self

  @classmethod
  def fromNodelist(klass, array, closed=True):
    """Construct a path from an array of Node objects."""
    self = klass()
    for a in array: assert(isinstance(a, Node))
    self.closed = closed
    self.activeRepresentation = NodelistRepresentation(self,array)
    self.asSegments() # Resolves a few problems
    return self

  @classmethod
  def fromGlyphsLayer(klass, layer):
    """Returns an *array of BezierPaths* from a Glyphs GSLayer object."""
    from beziers.path.representations.GSPath import GSPathRepresentation

    bezpaths = []
    for p in layer.paths:
      path = BezierPath()
      path.activeRepresentation = GSPathRepresentation(path,p)
      bezpaths.append(path)
    return bezpaths

  @classmethod
  def fromDrawable(klass, layer, *penArgs, **penKwargs):
    """Returns an *array of BezierPaths* from any object conforming to the pen protocol."""
    from beziers.utils.pens import BezierPathCreatingPen
    pen = BezierPathCreatingPen(*penArgs, **penKwargs)
    layer.draw(pen)
    return pen.paths

  @classmethod
  def fromFonttoolsGlyph(klass,font,glyphname):
    """Returns an *array of BezierPaths* from a FontTools font object and glyph name."""
    glyphset = font.getGlyphSet()
    from beziers.utils.pens import BezierPathCreatingPen
    pen = BezierPathCreatingPen(glyphset)
    _glyph = font.getGlyphSet()[glyphname]._glyph
    if "glyf" in font:
      _glyph.draw(pen, font["glyf"])
    else:
      _glyph.draw(pen)
    return pen.paths

  def asSegments(self):
    """Return the path as an array of segments (either Line, CubicBezier,
    or, if you are exceptionally unlucky, QuadraticBezier objects)."""
    if not isinstance(self.activeRepresentation, SegmentRepresentation):
      nl = self.activeRepresentation.toNodelist()
      assert isinstance(nl, list)
      self.activeRepresentation = SegmentRepresentation.fromNodelist(self,nl)
    return self.activeRepresentation.data()

  def asNodelist(self):
    """Return the path as an array of Node objects."""
    if not isinstance(self.activeRepresentation, NodelistRepresentation):
      nl = self.activeRepresentation.toNodelist()
      assert isinstance(nl, list)
      self.activeRepresentation = NodelistRepresentation(self,nl)
    return self.activeRepresentation.data()

  def asSVGPath(self):
    """Return the path as a string suitable for a SVG <path d="..."? element."""
    segs = self.asSegments()
    pathParts = ["M %f %f" % (segs[0][0].x, segs[0][0].y)]

    operators = "xxLQC"
    for s in segs:
      op = operators[len(s)] + " "
      for pt in s[1:]:
        op = op + "%f %f " % (pt.x, pt.y)
      pathParts.append(op)
    if self.closed:
      pathParts.append("Z")

    return " ".join(pathParts)

  def asMatplot(self):
    from matplotlib.path import Path
    nl = self.asNodelist()
    verts = [(nl[0].x,nl[0].y)]
    codes = [Path.MOVETO]

    for i in range(1,len(nl)):
      n = nl[i]
      verts.append((n.x,n.y))
      if n.type == "offcurve":
        if nl[i+1].type == "offcurve" or nl[i-1].type == "offcurve":
          codes.append(Path.CURVE4)
        else:
          codes.append(Path.CURVE3)
      elif n.type == "curve":
        if nl[i-1].type == "offcurve" and i >2 and nl[i-2].type == "offcurve":
          codes.append(Path.CURVE4)
        else:
          codes.append(Path.CURVE3)
      elif n.type == "line":
        codes.append(Path.LINETO)
      else:
        raise "Unknown node type"
    if self.closed:
      verts.append((nl[0].x,nl[0].y))
      codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)

  def plot(self,ax, **kwargs):
    """Plot the path on a Matplot subplot which you supply

    ::

          import matplotlib.pyplot as plt
          fig, ax = plt.subplots()
          path.plot(ax)

    """
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.path import Path
    import matplotlib.patches as patches
    path = self.asMatplot()
    if not "lw" in kwargs:
      kwargs["lw"] = 2
    if not "fill" in kwargs:
      kwargs["fill"] = False
    drawNodes = (not("drawNodes" in kwargs) or kwargs["drawNodes"] != False)
    if "drawNodes" in kwargs:
      kwargs.pop("drawNodes")
    patch = patches.PathPatch(path, **kwargs)
    ax.add_patch(patch)
    left, right = ax.get_xlim()
    top, bottom = ax.get_ylim()
    bounds = self.bounds()
    bounds.addMargin(50)
    if not (left == 0.0 and right == 1.0 and top == 0.0 and bottom == 1.0):
      bounds.extend(Point(left,top))
      bounds.extend(Point(right,bottom))
    ax.set_xlim(bounds.left,bounds.right)
    ax.set_ylim(bounds.bottom,bounds.top)
    if drawNodes:
      nl = self.asNodelist()
      for i in range(0,len(nl)):
        n = nl[i]
        if n.type =="offcurve":
          circle = plt.Circle((n.x, n.y), 2, fill=True,color="black",alpha=0.5)
          ax.add_artist(circle)
          if i+1 < len(nl) and nl[i+1].type != "offcurve":
            l = Line2D([n.x, nl[i+1].x], [n.y, nl[i+1].y], linewidth=2,color="black",alpha=0.3)
            ax.add_artist(l)
          if i-0 >= 0 and nl[i-1].type != "offcurve":
            l = Line2D([n.x, nl[i-1].x], [n.y, nl[i-1].y], linewidth=2,color="black",alpha=0.3)
            ax.add_artist(l)
        else:
          circle = plt.Circle((n.x, n.y), 3,color="black",alpha=0.3)
          ax.add_artist(circle)

  def clone(self):
    """Return a new path which is an exact copy of this one"""
    p = BezierPath.fromSegments(self.asSegments())
    p.closed = self.closed
    return p

  def round(self):
    """Rounds the points of this path to integer coordinates."""
    segs = self.asSegments()
    for s in segs: s.round()
    self.activeRepresentation = SegmentRepresentation(self,segs)

  def bounds(self):
    """Determine the bounding box of the path, returned as a
    `BoundingBox` object."""
    bbox = BoundingBox()
    for seg in self.asSegments():
      bbox.extend(seg)
    return bbox

  def splitAtPoints(self,splitlist):
    def mapx(v,ds): return (v-ds)/(1-ds)
    segs = self.asSegments()
    newsegs = []
    # Cluster splitlist by seg
    newsplitlist = {}
    for (seg,t) in splitlist:
      if not seg in newsplitlist: newsplitlist[seg] = []
      newsplitlist[seg].append(t)
    for k in newsplitlist:
      newsplitlist[k] = sorted(newsplitlist[k])
    # Now walk the path
    for seg in segs:
      if seg in newsplitlist:
        tList = newsplitlist[seg]
        while len(tList) > 0:
          t = tList.pop(0)
          if t < 1e-8: continue
          seg1,seg2 = seg.splitAtTime(t)
          newsegs.append(seg1)
          seg = seg2
          for i in range(0,len(tList)): tList[i] = mapx(tList[i],t)
      newsegs.append(seg)
    self.activeRepresentation = SegmentRepresentation(self,newsegs)


  def addExtremes(self):
    """Add extreme points to the path."""
    def mapx(v,ds): return (v-ds)/(1-ds)
    segs = self.asSegments()
    splitlist = []
    for seg in segs:
      for t in seg.findExtremes():
        splitlist.append((seg,t))
    self.splitAtPoints(splitlist)
    return self

  @property
  def length(self):
    """Returns the length of the whole path."""
    segs = self.asSegments()
    length = 0
    for s in segs: length += s.length
    return length

  def pointAtTime(self,t):
    """Returns the point at time t (0->1) along the curve, where 1 is the end of the whole curve."""
    segs = self.asSegments()
    if t == 1.0:
      return segs[-1].pointAtTime(1)
    t *= len(segs)
    seg = segs[int(math.floor(t))]
    return seg.pointAtTime(t-math.floor(t))

  def lengthAtTime(self,t):
    """Returns the length of the subset of the path from the start
    up to the point t (0->1), where 1 is the end of the whole curve."""
    segs = self.asSegments()
    t *= len(segs)
    length = 0
    for s in segs[:int(math.floor(t))]: length += s.length
    seg = segs[int(math.floor(t))]
    s1,s2 = seg.splitAtTime(t-math.floor(t))
    length += s1.length
    return length

  def offset(self, vector, rotateVector = True):
    """Returns a new BezierPath which approximates offsetting the
    current Bezier path by the given vector. Note that the vector
    will be rotated around the normal of the curve so that the
    offsetting always happens on the same 'side' of the curve:

..  figure:: offset1.png
    :scale: 75 %
    :alt: offset1

    If you don't want that and you want 'straight' offsetting instead
    (which may intersect with the original curve), pass
    `rotateVector=False`:

..  figure:: offset2.png
    :scale: 75 %
    :alt: offset1

    """
    # Method 1 - curve fit
    newsegs = []
    points = []
    def finishPoints(newsegs, points):
      if len(points) > 0:
        bp = BezierPath.fromPoints(points, error=0.1, cornerTolerance= 1)
        newsegs.extend(bp.asSegments())
      while len(points)>0:points.pop()

    for seg in self.asSegments():
      if isinstance(seg,Line):
        finishPoints(newsegs,points)
        newsegs.append(seg.translated(vector))
      else:
        t = 0.0
        while t <1.0:
          if rotateVector:
            points.append( seg.pointAtTime(t) + vector.rotated(Point(0,0), seg.normalAtTime(t).angle))
          else:
            points.append( seg.pointAtTime(t) + vector)
          step = max(abs(seg.curvatureAtTime(t)),0.1)
          t = t + min(seg.length / step,0.1)
    finishPoints(newsegs,points)
    newpath = BezierPath()
    newpath.activeRepresentation = SegmentRepresentation(newpath, newsegs)
    return newpath

  def append(self, other, joinType="line"):
    """Append another path to this one. If the end point of the first
    path is not the same as the start point of the other path, a line
    will be drawn between them."""
    segs1 = self.asSegments()
    segs2 = other.asSegments()
    if len(segs1) < 1:
      self.activeRepresentation = SegmentRepresentation(self, segs2)
      return
    if len(segs2) < 1:
      self.activeRepresentation = SegmentRepresentation(self, segs1)
      return

    # Which way around should they go?
    dist1 = segs1[-1].end.distanceFrom(segs2[0].start)
    dist2 = segs1[-1].end.distanceFrom(segs2[-1].end)
    if dist2 > 2 * dist1:
      segs2 = list(reversed([ x.reversed() for x in segs2]))

    # Add a line between if they don't match up
    if segs1[-1].end != segs2[0].start:
      segs1.append(Line(segs1[-1].end,segs2[0].start))

    # XXX Check for discontinuities and harmonize if needed

    segs1.extend(segs2)
    self.activeRepresentation = SegmentRepresentation(self, segs1)
    return self

  def reverse(self):
    """Reverse this path (mutates path)."""
    seg2 = [ x.reversed() for x in self.asSegments()]
    self.activeRepresentation = SegmentRepresentation(self, list(reversed(seg2)))
    return self

  def translate(self, vector):
    """Translates the path by a given vector."""
    seg2 = [ x.translated(vector) for x in self.asSegments()]
    self.activeRepresentation = SegmentRepresentation(self, seg2)
    return self

  def rotate(self, about, angle):
    """Rotate the path by a given vector."""
    seg2 = [ x.rotated(about, angle) for x in self.asSegments()]
    self.activeRepresentation = SegmentRepresentation(self, seg2)
    return self

  def scale(self, by):
    """Scales the path by a given magnitude."""
    seg2 = [ x.scaled(by) for x in self.asSegments()]
    self.activeRepresentation = SegmentRepresentation(self, seg2)
    return self

  def balance(self):
    """Performs Tunni balancing on the path."""
    segs = self.asSegments()
    for x in segs:
      if isinstance(x, CubicBezier): x.balance()
    self.activeRepresentation = SegmentRepresentation(self, segs)
    return self

  def findDiscontinuities(self):
    """Not implemented yet"""

  def harmonize(self):
    """Not implemented yet"""

  def roundCorners(self):
    """Not implemented yet"""

  def dash(self, lineLength = 50, gapLength = None):
    """Returns a list of BezierPath objects created by chopping
    this path into a dashed line::

      paths = path.dash(lineLength = 20, gapLength = 50)

..  figure:: dash.png
    :scale: 75 %
    :alt: path.dash(lineLength = 20, gapLength = 50)

"""
    if not gapLength:
      gapLength = lineLength
    granularity = self.length
    newpaths = []
    points = []
    for t in self.regularSampleTValue(granularity):
      lenSoFar = self.lengthAtTime(t) # Super inefficient. But simple!
      lenSoFar = lenSoFar % (lineLength + gapLength)
      if lenSoFar >= lineLength and len(points) > 0:
        # When all you have is a hammer...
        bp = BezierPath.fromPoints(points, error=1, cornerTolerance= 1)
        points = []
        if len(bp.asSegments()) > 0: newpaths.append(bp)
      elif lenSoFar <= lineLength:
        points.append(self.pointAtTime(t))
    return newpaths

  def segpairs(self):
    segs = self.asSegments()
    for i in range(0,len(segs)-1):
      yield (segs[i],segs[i+1])

  def harmonize(self, seg1, seg2):
    if seg1.end.x != seg2.start.x or seg1.end.y != seg2.start.y: return
    a1, a2 = seg1[1], seg1[2]
    b1, b2 = seg2[1], seg2[2]
    intersections = Line(a1,a2).intersections(Line(b1,b2),limited=False)
    if not intersections[0]: return
    p0 = a1.distanceFrom(a2) / a2.distanceFrom(intersections[0].point)
    p1 = b1.distanceFrom(intersections[0].point) / b1.distanceFrom(b2)
    r = math.sqrt(p0 * p1)
    t = r / (r+1)
    newA3 = a2.lerp(b1, t)
    fixup = seg2.start - newA3
    seg1[2] += fixup
    seg2[1] += fixup

  def flatten(self,degree=8):
    segs = []
    for s in self.asSegments():
      segs.extend(s.flatten(degree))
    return BezierPath.fromSegments(segs)

  def windingNumberOfPoint(self,pt):
    bounds = self.bounds()
    bounds.addMargin(10)
    ray1 = Line(Point(bounds.left,pt.y),pt)
    ray2 = Line(Point(bounds.right,pt.y),pt)
    leftIntersections = {}
    rightIntersections = {}
    leftWinding = 0
    rightWinding = 0
    for s in self.asSegments():
      for i in s.intersections(ray1):
        # print("Found left intersection with %s: %s" % (ray1, i.point))
        leftIntersections[i.point] = i

      for i in s.intersections(ray2):
        rightIntersections[i.point] = i

    for i in leftIntersections.values():
      # XXX tangents here are all positive? Really?
      # print(i.seg1, i.t1, i.point)
      tangent = s.tangentAtTime(i.t1)
      # print("Tangent at left intersection %s is %f" % (i.point,tangent.y))
      leftWinding += int(math.copysign(1,tangent.y))

    for i in rightIntersections.values():
      tangent = s.tangentAtTime(i.t1)
      # print("Tangent at right intersection %s is %f" % (i.point,tangent.y))
      rightWinding += int(math.copysign(1,tangent.y))

    # print("Left winding: %i right winding: %i " % (leftWinding,rightWinding))
    return max(abs(leftWinding),abs(rightWinding))

  def pointIsInside(self,pt):
    """Returns true if the given point lies on the "inside" of the path,
    assuming an 'even-odd' winding rule where self-intersections are considered
    outside."""
    li = self.windingNumberOfPoint(pt)
    return li % 2 == 1

  @property
  def signed_area(self):
    """Approximates the area under a closed path by flattening and treating as a polygon.
    Returns the signed area; positive means the path is counter-clockwise,
    negative means it is clockwise."""
    flat = self.flatten()
    area = 0
    for s in flat.asSegments():
      area = area + (s.start.x * s.end.y) - (s.start.y * s.end.x)
    area = area / 2.0
    return area

  @property
  def area(self):
    """Approximates the area under a closed path by flattening and treating as a
    polygon. Returns the unsigned area. Use :py:meth:`signed_area` if you want
    the signed area."""
    return abs(self.signed_area)

  @property
  def direction(self):
    """Returns the direction of the path: -1 for clockwise and 1 for counterclockwise."""
    return math.copysign(1, self.signed_area)

  @property
  def centroid(self):
    if not self.closed: return None
    return self.bounds().centroid # Really?

  def drawWithBrush(self, other):
    """Assuming that `other` is a closed Bezier path representing a pen or
    brush of a certain shape and that `self` is an open path, this method
    traces the brush along the path, returning an array of Bezier paths.

    `other` may also be a function which, given a time `t` (0-1), returns a closed
    path representing the shape of the brush at the given time.

    This requires the `shapely` library to be installed.
    """
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    polys = []
    samples = self.sample(self.length/2)
    def constantBrush(t):
      return other

    brush = other
    if not callable(brush):
      brush = constantBrush

    c = brush(0).centroid

    from itertools import tee
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    t = 0
    for n in samples:
      brushHere = brush(t).clone().flatten()
      brushHere.translate(n-brushHere.centroid)
      polys.append( Polygon([ (x[0].x, x[0].y) for x in brushHere.asSegments() ]) )
      t = t + 1.0/len(samples)
    concave_hull = unary_union(polys)
    ll = []
    for x,y in pairwise(concave_hull.exterior.coords):
      l = Line(Point(x[0],x[1]),Point(y[0],y[1]))
      ll.append(l)
    paths = [ BezierPath.fromSegments(ll) ]

    for interior in concave_hull.interiors:
      ll = []
      for x,y in pairwise(interior.coords):
        l = Line(Point(x[0],x[1]),Point(y[0],y[1]))
        ll.append(l)
      paths.append( BezierPath.fromSegments(ll) )

    return paths

  def quadraticsToCubics(self):
    """Converts all quadratic segments in the path to cubic Beziers."""
    segs = self.asSegments()
    for i,s in enumerate(segs):
      if len(s) == 3:
        segs[i] = s.toCubicBezier()
    return self

  def thicknessAtX(path, x):
    """Returns the thickness of the path at x-coordinate ``x``."""
    bounds = path.bounds()
    bounds.addMargin(10)
    ray = Line(Point(x - 0.1, bounds.bottom), Point(x + 0.1, bounds.top))
    intersections = []
    for seg in path.asSegments():
      intersections.extend(seg.intersections(ray))
    if len(intersections) < 2:
      return None
    intersections = list(sorted(intersections, key=lambda i: i.point.y))
    i1, i2 = intersections[0:2]
    inorm1 = i1.seg1.normalAtTime(i1.t1)
    ray1 = Line(i1.point + (inorm1 * 1000), i1.point + (inorm1 * -1000))
    iii = i2.seg1.intersections(ray1)
    if iii:
      ll1 = i1.point.distanceFrom(iii[0].point)
    else:
      # Simple, vertical version
      return abs(i1.point.y - i2.point.y)

    inorm2 = i2.seg1.normalAtTime(i2.t1)
    ray2 = Line(i2.point + (inorm2 * 1000), i2.point + (inorm2 * -1000))
    iii = i1.seg1.intersections(ray2)
    if iii:
      ll2 = i2.point.distanceFrom(iii[0].point)
      return (ll1 + ll2) * 0.5
    else:
      return ll1

    # midpoint = (i1.point + i2.point) / 2
    # # Find closest path to midpoint
    # # Find the tangent at that time
    # inorm2 = i2.seg1.normalAtTime(i2.t1)

  def distanceToPath(self, other, samples = 10):
    """Finds the distance to the other curve at its closest point,
    along with the t values for the closest point at each segment
    and the relevant segments.

    Returns: ``distance, t1, t2, seg1, seg2``."""
    from beziers.utils.curvedistance import curveDistance
    segs1 = self.asSegments()
    segs2 = other.asSegments()
    minDistance = None
    # Find closest segment pair.
    for s1 in segs1:
      samples1 = s1.sample(samples)
      for s2 in segs2:
        samples2 = s2.sample(samples)
        d = min([ p1.squareDistanceFrom(p2) for p1 in samples1 for p2 in samples2])
        if not minDistance or d < minDistance:
          minDistance = d
          closestPair = (s1,s2)
    c = curveDistance(closestPair[0], closestPair[1])
    return (c[0],c[1],c[2], closestPair[0], closestPair[1])

  def tidy(self, **kwargs):
    """Tidies a curve by adding extremes, and then running
    ``removeIrrelevantSegments`` and ``smooth``. ``relLength``,
    ``absLength``, ``maxCollectionSize``, ``lengthLimit`` and
    ``cornerTolerance`` parameters are passed to the relevant routine."""
    self.addExtremes()
    self.removeIrrelevantSegments(**{k:v for k,v in kwargs.items()
      if k in ["relLength", "absLength"] })
    self.smooth(**{k:v for k,v in kwargs.items()
      if k in ["maxCollectionSize", "lengthLimit", "cornerTolerance"] })

  def removeIrrelevantSegments(self, relLength=1/50000, absLength=0):
    """Removes small and collinear line segments. Collinear line
    segments are adjacent line segments which are heading in the same
    direction, and hence can be collapsed into a single segment.
    Small segments (those less than ``absLength`` units, or less than
    ``relLength`` as a fraction of the path's total length) are
    removed entirely."""
    segs = self.asSegments()
    newsegs = [segs[0]]
    smallLength = self.length * relLength
    for i in range(1,len(segs)):
      prev = newsegs[-1]
      this = segs[i]
      if this.length < smallLength or this.length < absLength:
        this[0] = prev[0]
        newsegs[-1] = this
        continue
      if len(prev) == 2 and len(this) == 2:
        if math.isclose(prev.tangentAtTime(0).angle, this.tangentAtTime(0).angle):
          this[0] = prev[0]
          newsegs[-1] = this
          continue
      newsegs.append(this)
    self.activeRepresentation = SegmentRepresentation(self, newsegs)
    return self

  def smooth(self, maxCollectionSize = 30, lengthLimit = 20, cornerTolerance = 10):
    """Smooths a curve, by collating lists of small (at most ``lengthLimit``
    units long) segments at most ``maxCollectionSize`` segments at a time,
    and running them through a curve fitting algorithm. The list collation
    also stops when one segment turns more than ``cornerTolerance`` degrees
    away from the previous one, so that corners are not smoothed."""
    smallLineLength = lengthLimit
    segs = self.asSegments()
    i = 0
    collection = []
    while i < len(segs):
        s = segs[i]
        if s.length < smallLineLength and len(collection) <= maxCollectionSize:
          collection.append(s)
        else:
          corner = False
          if len(collection) > 1:
            last = collection[-1]
            if abs(last.tangentAtTime(1).angle - s.tangentAtTime(0).angle) > math.radians(cornerTolerance):
              corner = True
          if len(collection) > maxCollectionSize or corner or i == len(segs)-2:
            points = [x.start for x in collection]
            bp = BezierPath.fromPoints(points)
            if len(bp.asSegments()) > 0:
              segs[i-len(collection):i] = bp.asSegments()
              i -= len(collection)
            collection = []
        i += 1
    if len(collection) > 0:
      points = [x.start for x in collection]
      bp = BezierPath.fromPoints(points)
      if len(bp.asSegments()) > 0:
        segs[i-(1+len(collection)):i-1] = bp.asSegments()

    self.activeRepresentation = SegmentRepresentation(self, segs)
    return self
