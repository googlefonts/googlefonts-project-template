from beziers.line import Line
from beziers.cubicbezier import CubicBezier
from beziers.path import BezierPath
from beziers.path.representations.Nodelist import NodelistRepresentation, Node

class FontParts:
  @classmethod
  def fromFontpartsGlyph(klass, glyph):
    """Returns an *array of BezierPaths* from a FontParts glyph object."""
    paths = []
    if hasattr(glyph, "contours"):
      contouriterator = glyph.contours
    else:
      contouriterator = glyph
    for c in contouriterator:
      path = BezierPath()
      path.closed = False
      nodeList = []
      if hasattr(c, "points"):
        pointiterator = c.points
      else:
        pointiterator = c
      for p in pointiterator:
        if hasattr(p, "segmentType"):
          t = p.segmentType
        else:
          t = p.type
        nodeList.append(Node(p.x,p.y,t))
      path.activeRepresentation = NodelistRepresentation(path, nodeList)
      if nodeList[0].point == nodeList[-1].point:
        path.closed = True
      paths.append(path)
    return paths

  @classmethod
  def drawToFontpartsGlyph(klass,glyph,path):
    pen = glyph.getPen()
    segs = path.asSegments()
    pen.moveTo((segs[0][0].x,segs[0][0].y))
    for seg in segs:
      if isinstance(seg, Line):
        pen.lineTo((seg[1].x,seg[1].y))
      elif isinstance(seg, CubicBezier):
        pen.curveTo(
          (seg[1].x,seg[1].y),
          (seg[2].x,seg[2].y),
          (seg[3].x,seg[3].y))
    if path.closed:
      pen.closePath()
