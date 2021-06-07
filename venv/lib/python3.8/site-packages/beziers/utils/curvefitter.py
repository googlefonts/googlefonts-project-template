from beziers.point import Point
from beziers.cubicbezier import CubicBezier
import sys
import math

def B0(u):
  return (1.0 - u) * (1.0 - u) * (1.0 - u)

def B1(u):
  return 3 * u * (1.0 - u) * (1.0 - u)

def B2(u):
  return 3 * u * u * (1.0 - u)

def B3(u):
  return u * u * u


class CurveFit:
  # Algorithm lifted from Inkscape

  @classmethod
  def fitCurve(self, data, error, cornerTolerance, maxSegments):
    # We want to uniqify the points but maintaining order
    # (so we can't use a set). An ordered set would be too heavy for this.
    keys = {}
    def filterSeen(x):
      if hash(x) in keys: return False
      keys[hash(x)] = 1
      return True
    data = list(filter(filterSeen, data))
    if len(data) < 2: return
    return self._fitCurve(data, None, None, error, cornerTolerance, maxSegments)

  @classmethod
  def fitLine(self, data, tHat1, tHat2):
    p0, p3 = data[0], data[-1]
    dist = p0.distanceFrom(p3)/3.0

    if tHat1:
      p1 = p0 + tHat1 * dist
    else:
      p1 = ((p0 * 2.0) + p3) / 3.0
    if tHat2:
      p2 = p3 + tHat2 * dist
    else:
      p2 = ((p3 * 2.0) + p0) / 3.0

    return CubicBezier(p0, p1, p2, p3)

  @classmethod
  def estimateBi(self, bez, data, u):
    num = Point(0, 0)
    den = 0.0
    for (coeff, datum) in zip(u, data):
      b0,b1,b2,b3 =  B0(coeff), B1(coeff), B2(coeff), B3(coeff)
      num.x += b1 * (b0 * bez[0].x + b2 * bez[2].x + b3 * bez[3].x - datum.x)
      num.y += b1 * (b0 * bez[0].y + b2 * bez[2].y + b3 * bez[3].y - datum.y)
      den -= b1 * b1

    if den != 0.0:
      bez[1] = num/den
    else:
      bez[1] = bez[0].lerp(bez[3], 1/3.0)

  @classmethod
  def _leftTangent(self, data):
    return (data[1]-data[0]).toUnitVector()

  @classmethod
  def _rightTangent(self, data):
    return (data[-1]-data[-2]).toUnitVector()

  @classmethod
  def centerTangent(self, data, center):
    if data[center + 1] == data[center-1]:
      ret = data[center] - data[center - 1]
      ret.rotate(Point(0,0), math.pi / 2.0)
      return ret.toUnitVector()
    else:
      ret = data[center - 1] - data[center+1]
      return ret.toUnitVector()

  @classmethod
  def leftTangent(self, data, tolerance):
    i = 1
    while True:
      pi = data[i]
      t = pi - data[0]
      distSq = t.__matmul__(t)
      if (tolerance < distSq): return t.toUnitVector()
      i = i + 1
      if i == len(data):
        if distSq == 0: return self._leftTangent(data)
        else: return t.toUnitVector()

  @classmethod
  def rightTangent(self, data, tolerance):
    i = len(data)-2
    while True:
      pi = data[i]
      t = pi - data[-1]
      distSq = t.__matmul__(t)
      if (tolerance < distSq): return t.toUnitVector()
      i = i - 1
      if i == 0:
        if distSq == 0: return self._rightTangent(data)
        else: return t.toUnitVector()

  @classmethod
  def generateBezier(self, data, u, tHat1, tHat2, tolerance_sq):
    est_tHat1 = tHat1
    est_tHat2 = tHat2
    if not est_tHat1:
      est_tHat1 = self.leftTangent(data, tolerance_sq)
    if not est_tHat2:
      est_tHat2 =  self.rightTangent(data, tolerance_sq)
    bez = self.estimateLengths(data, u, est_tHat1, est_tHat2)
    if not tHat1:
      # print("Refining estimate %s" % bez)
      self.estimateBi(bez, data, u)
      # print("Result of estimateBi %s" % bez)
      if bez[1].distanceFrom(bez[0]) > sys.float_info.epsilon:
        est_tHat1 = (bez[1]-bez[0]).toUnitVector()
      # print("tHat1 is now %s" % est_tHat1)
      bez = self.estimateLengths(data, u, est_tHat1, est_tHat2)
    return bez

  @classmethod
  def estimateLengths(self, data, u, tHat1, tHat2):
    C = [ [ 0.0, 0.0], [ 0.0, 0.0 ]]
    X = [ 0.0, 0.0 ]
    # bez = SCBezier()
    for (coeff,datum) in zip(u, data):
      (b0,b1,b2,b3) = (B0(coeff), B1(coeff), B2(coeff), B3(coeff))
      (a1, a2) = (tHat1 * b1, tHat2 * b2)
      C[0][0] += a1.__matmul__(a1)
      C[0][1] += a1.__matmul__(a2)
      C[1][0] = C[0][1]
      C[1][1] += a2.__matmul__(a2)
      s1 = data[0] * (b0+b1)
      shortfall = datum - s1
      shortfall = shortfall - (data[-1] * (b2+b3))
      X[0] += a1.__matmul__(shortfall)
      X[1] += a2.__matmul__(shortfall)

    det_C0_C1 = C[0][0] * C[1][1] - C[1][0] * C[0][1]
    if det_C0_C1 != 0.0:
      det_C0_X  = C[0][0] * X[1]    - C[0][1] * X[0]
      det_X_C1  = X[0]    * C[1][1] - X[1]    * C[0][1]
      alpha_l = det_X_C1 / det_C0_C1
      alpha_r = det_C0_X / det_C0_C1
    else:
      c0 = C[0][0] + C[0][1]
      if c0 != 0:
        alpha_l = X[0] / c0
        alpha_r = X[0] / c0
      else:
        alpha_l = 0.0
        alpha_r = 0.0
    if alpha_l < 1.0e-6 or alpha_r < 1.0e-6:
      alpha_l = data[-1].distanceFrom(data[0]) / 3.0
      alpha_r = alpha_l

    return CubicBezier(data[0],
                    tHat1 * alpha_l + data[0],
                    tHat2 * alpha_r + data[-1],
                    data[-1])

  @classmethod
  def chordLengthParameterize(self, points):
    u = [0.0]
    v = 0
    for i in range(1, len(points)):
      v += points[i].distanceFrom(points[i-1])
      u.append(v)
    return [ n/v for n in u ]

  @classmethod
  def newtonRaphsonFind(self, bez, point, u):
    q0 = bez.pointAtTime(u)
    q1 = bez.derivative().pointAtTime(u)
    q2 = bez.derivative().derivative().pointAtTime(u)
    diff = q0 - point
    numerator = diff.__matmul__(q1)
    denominator = (q1.__matmul__(q1)) + (diff.__matmul__(q2))
    if denominator > 0.0:
      improvedU = u - ( numerator / denominator )
    else:
      if numerator > 0.0:
        improvedU = u * 0.98 - 0.01
      elif numerator < 0.0:
        improvedU = 0.031 + u * 0.98
      else:
        improvedU = u

    if (improvedU < 0): improvedU = 0
    if (improvedU > 1): improvedU = 1
    dist2 = q0.distanceFrom(point)
    proportion = 0.125
    while True:
      proportion += 0.125
      newDistance2 = point.distanceFrom(bez.pointAtTime(improvedU))
      if newDistance2 > dist2:
        if proportion > 1.0:
          improvedU = u
          break
        improvedU = ( ( 1 - proportion ) * improvedU  + proportion * u)
      else:
       break
    return improvedU

  @classmethod
  def reparameterize(self, bez, points, params):
    for i in range(0, len(points)):
      params[i] = self.newtonRaphsonFind(bez, points[i], params[i])

  @classmethod
  def computeHook(self, ffrom, to, parameter, bez, cornerTolerance):
    p = bez.pointAtTime(parameter)
    dist = p.distanceFrom(ffrom.lerp(to, 0.5))
    if dist < cornerTolerance: return 0
    allowed = ffrom.distanceFrom(to) + cornerTolerance
    return dist / allowed

  @classmethod
  def computeMaxError(self, bez, points, params, tolerance, cornerTolerance):
    maxSqDist = 0.0
    maxHookRatio = 0.0
    splitPoint = 0
    snapEnd = 0
    prev = bez[0]
    for i in range(1, len(points)):
      cur = bez.pointAtTime(params[i])
      distSq = cur.squareDistanceFrom(points[i])
      if distSq > maxSqDist:
        maxSqDist = distSq
        splitPoint = i
      hookRatio = self.computeHook(prev, cur, (params[i]+params[i-1])/(2.0), bez, cornerTolerance)
      if maxHookRatio < hookRatio:
        maxHookRatio = hookRatio
        snapEnd = i
      prev = cur
    distRatio = math.sqrt(maxSqDist) / tolerance
    if maxHookRatio <= distRatio:
      return (distRatio, splitPoint)
    else:
      splitPoint = snapEnd-1
      return (-maxHookRatio, splitPoint)

  @classmethod
  def _fitCurve(self, points, tangent1, tangent2, error, cornerTolerance, maxSegments):
    if len(points) == 0: return
    if len(points) == 2:
      return [self.fitLine(points, tangent1, tangent2)]
    maxIterations = 3
    isCorner = False
    u = self.chordLengthParameterize(points)
    if u[-1] == 0.0: return []
    bez = self.generateBezier(points, u, tangent1, tangent2, error)
    self.reparameterize(bez, points, u)
    tolerance = math.sqrt(error + 1e-9)
    (maxErrorRatio, splitPoint) = self.computeMaxError(bez, points, u, tolerance, cornerTolerance)
    if abs(maxErrorRatio) <= 1.0: return [bez]
    if ( 0.0 <= maxErrorRatio and maxErrorRatio <= 3.0 ):
      for _ in range(0, maxIterations+1):
        bez = self.generateBezier(points, u, tangent1, tangent2, error)
        (maxErrorRatio, splitPoint) = self.computeMaxError( bez,  points,  u,  tolerance,  cornerTolerance)
        if abs(maxErrorRatio) <= 1.0: return [bez]

    isCorner = maxErrorRatio < 0
    if isCorner:
      if splitPoint == 0:
        if tangent1 is None:
          splitPoint = splitPoint + 1
        else:
          return self._fitCurve( points, Point(0.0,0.0), tangent2, error, cornerTolerance, maxSegments)

      elif splitPoint == len(points) - 1:
        if tangent2 is None:
          splitPoint = splitPoint - 1
        else:
          return self._fitCurve(points, tangent1, Point(0.0,0.0), error, cornerTolerance, maxSegments)

    if 1 < maxSegments:
      segmentsRemaining = maxSegments - 1
      if isCorner:
        if not (0 < splitPoint and splitPoint < len(points) - 1): return []
        recTHat1 = Point(0.0,0.0)
        recTHat2 = Point(0.0,0.0)
      else:
        recTHat2 = self.centerTangent(points, splitPoint)
        recTHat1 = recTHat2 * -1

      lPoints = points[:splitPoint+1]
      rPoints = points[splitPoint:]
      lbeziers = self._fitCurve(lPoints, tangent1, recTHat2, error, cornerTolerance, segmentsRemaining)
      if lbeziers:
        segmentsRemaining = segmentsRemaining - len(lbeziers)
      rbeziers = self._fitCurve(rPoints, recTHat1, tangent2, error, cornerTolerance, segmentsRemaining)
      return lbeziers + rbeziers
    else:
      return []
