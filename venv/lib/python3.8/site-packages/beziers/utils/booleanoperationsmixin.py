import sys
from beziers.path.representations.Segment import SegmentRepresentation
from beziers.utils.intersectionsmixin import Intersection
import logging
import pyclipper
from beziers.line import Line
from beziers.point import Point

class BooleanOperationsMixin:

  def getSelfIntersections(self):
    """Returns a list of a path's self-intersections as Intersection objects."""

    segs = self.asSegments()
    intersections = []
    for seg in segs:
      l = seg.hasLoop
      if l and l[0]>0 and l[0]<1 and l[1]>0 and l[0]<1:
        intersections.append(Intersection(seg,l[0], seg,l[1]))
    for i1 in range(0, len(segs)):
      for i2 in range (i1+1, len(segs)):
        for i in segs[i1].intersections(segs[i2]):
          if i.t1 > 1e-2 and i.t1 < 1-1e-2:
            intersections.append(i)
    return intersections

  def removeOverlap(self):
    """Resolves a path's self-intersections by 'walking around the outside'."""
    if not self.closed:
      raise "Can only remove overlap on closed paths"
    splitlist = []
    splitpoints = {}
    def roundoff(point):
      return (int(point.x*1),int(point.y*1))

    for i in self.getSelfIntersections():
      splitlist.append((i.seg1,i.t1))
      splitlist.append((i.seg2,i.t2))
      splitpoints[roundoff(i.point)] = {"in":[], "out": []}
    self.splitAtPoints(splitlist)
    # Trace path
    segs = self.asSegments()
    for i in range(0,len(segs)):
      seg = segs[i]
      if i < len(segs)-1:
        seg.next = segs[i+1]
      else:
        seg.next = segs[0]
      seg.visited = False
      segWinding = self.windingNumberOfPoint(seg.pointAtTime(0.5))
      seg.windingNumber = segWinding
      if roundoff(seg.end) in splitpoints:
        splitpoints[roundoff(seg.end)]["in"].append(seg)
      if roundoff(seg.start) in splitpoints:
        splitpoints[roundoff(seg.start)]["out"].append(seg)
    newsegs = []
    copying = True
    logging.debug("Split points:", splitpoints)
    seg = segs[0]
    while not seg.visited:
      logging.debug("Starting at %s, visiting %s" % (seg.start, seg))
      newsegs.append(seg)
      seg.visited = True
      if roundoff(seg.end) in splitpoints and len(splitpoints[roundoff(seg.end)]["out"]) > 0:
        logging.debug("\nI am at %s and have a decision: " % seg.end)
        inAngle = seg.tangentAtTime(1).angle
        logging.debug("My angle is %s" % inAngle)
        # logging.debug("Options are: ")
        # for s in splitpoints[roundoff(seg.end)]["out"]:
          # logging.debug(s.end, s.tangentAtTime(0).angle, self.windingNumberOfPoint(s.pointAtTime(0.5)))
        # Filter out the inside points
        splitpoints[roundoff(seg.end)]["out"] = [ o for o in splitpoints[roundoff(seg.end)]["out"] if o.windingNumber < 2]
        splitpoints[roundoff(seg.end)]["out"].sort(key = lambda x: x.tangentAtTime(0).angle-inAngle)
        seg = splitpoints[roundoff(seg.end)]["out"].pop(-1)
        # seg = seg.next
        # logging.debug("I chose %s\n" % seg)
      else:
        seg = seg.next

    self.activeRepresentation = SegmentRepresentation(self,newsegs)

  def clip(self,clip,cliptype, flat=False):
    splitlist1 = []
    splitlist2 = []
    intersections = {}
    cloned = self.clone()
    clip = clip.clone()

    # Split all segments at intersections
    for s1 in self.asSegments():
      for s2 in clip.asSegments():
        for i in s1.intersections(s2):
          if i.t1 > 1e-8 and i.t1 < 1-1e-8:
            if i.seg1 == s1:
              splitlist1.append((i.seg1,i.t1))
              splitlist2.append((i.seg2,i.t2))
            else:
              splitlist2.append((i.seg1,i.t1))
              splitlist1.append((i.seg2,i.t2))
            intersections[i.point] = i

    logging.debug("Split list: %s" % splitlist1)
    logging.debug("Split list 2: %s" % splitlist2)
    cloned.splitAtPoints(splitlist1)
    clip.splitAtPoints(splitlist2)
    logging.debug("Self:")
    logging.debug(cloned.asSegments())
    logging.debug("Clip:")
    logging.debug(clip.asSegments())

    segs1unflattened = cloned.asSegments()
    segs2unflattened = clip.asSegments()

    # Replace with flattened versions, building a dictionary of originals
    segs1 = []
    reconstructionLUT = {}
    precision = 100.

    def fillLUT(flats):
      for line in flats:
        key = ((line.start * precision).rounded(), (line.end * precision).rounded())
        reconstructionLUT[key] = (line._orig or line)
        key2 = ((line.end * precision).rounded(), (line.start * precision).rounded())
        reconstructionLUT[key2] = (line._orig or line).reversed()

    for s in segs1unflattened:
      flats = s.flatten(2)
      fillLUT(flats)
      segs1.extend(flats)

    segs2 = []
    for s in segs2unflattened:
      flats = s.flatten(2)
      fillLUT(flats)
      segs2.extend(flats)

    # Leave it to the professionals
    subj = [(s[0].x*precision, s[0].y*precision) for s in segs1]
    clip = [(s[0].x*precision, s[0].y*precision) for s in segs2]
    pc = pyclipper.Pyclipper()
    pc.AddPath(clip, pyclipper.PT_CLIP, True)
    pc.AddPath(subj, pyclipper.PT_SUBJECT, True)
    paths = pc.Execute(cliptype, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
    outpaths = []

    # Now reconstruct Bezier segments from flattened paths
    def pairwise(points):
      a = (p for p in points)
      b = (p for p in points)
      next(b)
      for curpoint,nextpoint in zip(a, b):
        yield curpoint, nextpoint

    newpaths = []
    from beziers.path import BezierPath
    for p in paths:
      newpath = []
      for scaledstart,scaledend in pairwise(p):
        key = (Point(*scaledstart), Point(*scaledend))
        if key in reconstructionLUT and not flat:
          orig = reconstructionLUT[key]
          if len(newpath) == 0 or newpath[-1] != orig:
            newpath.append(orig)
        else:
          newpath.append(Line(key[0]/precision, key[1]/precision))
      outpaths.append(BezierPath.fromSegments(newpath))
    return outpaths

  def union(self,other, flat=False):
    """Returns a list of Bezier paths representing the union of the two input paths."""
    return self.clip(other, pyclipper.CT_UNION, flat)

  def intersection(self,other, flat=False):
    """Returns a list of Bezier paths representing the intersection of the two input paths."""
    return self.clip(other, pyclipper.CT_INTERSECTION, flat)

  def difference(self,other, flat=False):
    """Returns a list of Bezier paths representing the first input path subtracted from the second."""
    return self.clip(other, pyclipper.CT_DIFFERENCE, flat)
