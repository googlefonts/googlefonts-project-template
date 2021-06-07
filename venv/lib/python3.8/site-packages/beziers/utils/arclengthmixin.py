from beziers.utils.legendregauss import Tvalues, Cvalues
import math

class ArcLengthMixin:
  @property
  def length(self):
    d = self.derivative()
    z = 0.5
    _sum = 0
    for i in range(0,len(Tvalues)):
      t = z * Tvalues[i] + z
      p = d.pointAtTime(t)
      arc = math.sqrt(p.x * p.x + p.y * p.y)
      _sum += Cvalues[i] * arc
    return _sum * z