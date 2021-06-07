from beziers.cubicbezier import CubicBezier
from beziers.quadraticbezier import QuadraticBezier
from beziers.line import Line
from beziers.point import Point
import math

"""
This implements (possibly badly) the algorithm in "Computing the
minimum distance between two Bézier curves", Chen et al.,
*Journal of Computational and Applied Mathematics* 229(2009) 294-301

I could not get the clever subdivision heuristic working (divide the
parameter space into two) but divided it into four instead. Using
their heuristic of dividing at i/2n instead of 1/2 does seem to give
better results, though. The checks for Property 1 and Property 2 never
seem to be fired either. So I'm probably doing something wrong.

The results look fine but there's probably more computations happening
than needed. I use memoization and an initial sanity check (whether
alpha is more than the current best alpha) to cut down on the
computations but I'm sure it could still be improved.
"""

def C(y, x):
    try:
        binom = math.factorial(x) // math.factorial(y) // math.factorial(x - y)
    except ValueError:
        binom = 0
    return binom


def A_r(r, P):
    n = len(P) - 1  # Order
    upsilon = min(r, n)
    theta = max(0, r - n)
    summand = 0
    for i in range(theta, upsilon + 1):
        summand += P[i].dot(P[r - i]) * C(i, n) * C(r - i, n) / C(r, 2 * n)
    return summand


B_k = A_r  # But with P -> Q, n -> m, r -> k


def C_rk(r, k, bez1, bez2):
    # These also have parallel factors
    def factor(P, r_or_k):
        n = len(P) - 1
        upsilon = min(r_or_k, n)
        theta = max(0, r_or_k - n)
        summand = Point(0, 0)
        for i in range(theta, upsilon + 1):
            summand += P[i] * C(i, n) * C(r_or_k - i, n) / C(r_or_k, 2 * n)
        return summand

    left = factor(bez1, r)
    right = factor(bez2, k)
    return left.dot(right)


def basis_function(n, i, u):
    res = C(i, n) * (1 - u) ** (n - i) * u ** i
    return res


class MinimumCurveDistanceFinder:
    def __init__(self, bez1, bez2):
        self.bez1 = bez1
        self.bez2 = bez2
        self.dCache = {}
        self.sCache = {}
        self.bestAlpha = None
        self.iterations = 0

    def D(self, r, k):
        if (r, k) not in self.dCache:
            self.dCache[(r, k)] = (
                A_r(r, self.bez1)
                + B_k(k, self.bez2)
                - 2 * C_rk(r, k, self.bez1, self.bez2)
            )
        return self.dCache[(r, k)]

    def S(self, u, v):  # u,v are times
        if (u, v) in self.sCache:
            return self.sCache[(u, v)]

        n = len(self.bez1) - 1
        m = len(self.bez2) - 1

        summand = 0
        for r in range(0, 2 * n + 1):
            for k in range(0, 2 * m + 1):
                summand += (
                    self.D(r, k)
                    * basis_function(2 * n, r, u)
                    * basis_function(2 * m, k, v)
                )
        self.sCache[(u, v)] = summand
        return summand

    def minDist(self, uinterval=(0, 1), vinterval=(0, 1), epsilon=0.001):
        n = len(self.bez1) - 1
        m = len(self.bez2) - 1
        self.iterations = self.iterations + 1
        umin, umax = uinterval
        vmin, vmax = vinterval
        umid = (umin + umax) / 2
        vmid = (vmin + vmax) / 2
        svalues = [
            [self.S(umin, vmin), umin, vmin],
            [self.S(umin, vmax), umin, vmax],
            [self.S(umax, vmin), umax, vmin],
            [self.S(umax, vmax), umax, vmax],
        ]
        alpha = min(svalues, key=lambda x: x[0])[0]
        if self.bestAlpha and alpha > self.bestAlpha:
            return [alpha, umid, vmid]
        self.bestAlpha = alpha

        if abs(umax - umin) <= epsilon or abs(vmax - vmin) <= epsilon:
            return [alpha, umid, vmid]

        # # Property 1: Check if any D(r>k) < alpha
        # # Also find out where the min value is for division
        isOutside = True
        minDRK = None
        minIJ = (None, None)
        for r in range(0, 2 * n):
            for k in range(0, 2 * m):
                drk = self.D(r, k)
                if drk < alpha:
                    isOutside = False
                if not minDRK or drk < minDRK:
                    minDrk = drk
                    minIJ = (r, k)
        if isOutside:
            return [alpha, umid, vmid]

        # This one never seems to work

        # # Property 2: Boundary check
        atBoundary0onBez1 = True
        atBoundary1onBez1 = True
        atBoundary0onBez2 = True
        atBoundary1onBez2 = True
        for i in range(0, 2 * n):
            for j in range(0, 2 * m):
                dij = self.D(i, j)
                dkj = self.D(0, j)
                if dij < dkj:
                    atBoundary0onBez1 = False
                dkj = self.D(2 * n, j)
                if dij < dkj:
                    atBoundary1onBez1 = False
                dkj = self.D(i, 0)
                if dij < dkj:
                    atBoundary0onBez2 = False
                dkj = self.D(i, 2 * n)
                if dij < dkj:
                    atBoundary1onBez2 = False
        if atBoundary0onBez1 and atBoundary0onBez2:
            return svalues[0]
        if atBoundary0onBez1 and atBoundary1onBez2:
            return svalues[1]
        if atBoundary1onBez1 and atBoundary0onBez2:
            return svalues[2]
        if atBoundary1onBez1 and atBoundary1onBez2:
            return svalues[3]

        newuMid = umin + (umax - umin) * (minIJ[0] / (2 * n))
        newvMid = vmin + (vmax - vmin) * (minIJ[1] / (2 * m))

        # Subdivision
        r1 = self.minDist(uinterval=(umin, newuMid), vinterval=(vmin, newvMid))
        r2 = self.minDist(uinterval=(umin, newuMid), vinterval=(newvMid, vmax))
        r3 = self.minDist(uinterval=(newuMid, umax), vinterval=(vmin, newvMid))
        r4 = self.minDist(uinterval=(newuMid, umax), vinterval=(newvMid, vmax))
        results = min([r1, r2, r3, r4], key=lambda x: x[0])
        return results

def curveDistance(bez1,bez2):
    """Find the distance between two curves."""
    c = MinimumCurveDistanceFinder(bez1, bez2)
    dist, t1, t2 = c.minDist()
    return math.sqrt(dist), t1, t2

if __name__ == "__main__":
    bez1 = CubicBezier(
        Point(129, 139), Point(190, 139), Point(201, 364), Point(90, 364)
    )
    bez2 = CubicBezier(
        Point(309, 159), Point(178, 159), Point(215, 408), Point(309, 408)
    )
    bez3 = Line(Point(309, 159), Point(309, 408))

    c = MinimumCurveDistanceFinder(bez1, bez3)
    dist, t1, t2 = c.minDist()
    print(bez1.pointAtTime(t1))
    print(bez3.pointAtTime(t2))
    print(math.sqrt(dist))
    print(c.iterations)
