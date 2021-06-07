import math
from beziers.utils import isclose

class AffineTransformation(object):
  def __init__(self, matrix = None):
    if not matrix:
      self.matrix = [
        [ 1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, 1]
      ]
    else:
      self.matrix = matrix

  def __str__(self):
    m = self.matrix
    return "[ {:> 8.3f} {:> 8.3f} {:> 8.3f} ],\n[ {:> 8.3f} {:> 8.3f} {:> 8.3f} ],\n[ {:> 8.3f} {:> 8.3f} {:> 8.3f} ]".format(
      m[0][0],m[0][1],m[0][2],m[1][0],m[1][1],m[1][2],m[2][0],m[2][1],m[2][2])

  def apply(self, other):
    m1 = self.matrix
    m2 = other.matrix
    self.matrix =[[m1[0][0] * m2[0][0] + m1[0][1] * m2[1][0] + m1[0][2] * m2[2][0], 
      m1[0][0] * m2[0][1] + m1[0][1] * m2[1][1] + m1[0][2] * m2[2][1], 
      m1[0][0] * m2[0][2] + m1[0][1] * m2[1][2] + m1[0][2] * m2[2][2]],
      [m1[1][0] * m2[0][0] + m1[1][1] * m2[1][0] + m1[1][2] * m2[2][0],
      m1[1][0] * m2[0][1] + m1[1][1] * m2[1][1] + m1[1][2] * m2[2][1], 
      m1[1][0] * m2[0][2] + m1[1][1] * m2[1][2] + m1[1][2] * m2[2][2]],
      [m1[2][0] * m2[0][0] + m1[2][1] * m2[1][0] + m1[2][2] * m2[2][0],
      m1[2][0] * m2[0][1] + m1[2][1] * m2[1][1] + m1[2][2] * m2[2][1], 
      m1[2][0] * m2[0][2] + m1[2][1] * m2[1][2] + m1[2][2] * m2[2][2]]]

  def apply_backwards(self, other):
    m2 = self.matrix
    m1 = other.matrix
    self.matrix =[[m1[0][0] * m2[0][0] + m1[0][1] * m2[1][0] + m1[0][2] * m2[2][0], 
      m1[0][0] * m2[0][1] + m1[0][1] * m2[1][1] + m1[0][2] * m2[2][1], 
      m1[0][0] * m2[0][2] + m1[0][1] * m2[1][2] + m1[0][2] * m2[2][2]],
      [m1[1][0] * m2[0][0] + m1[1][1] * m2[1][0] + m1[1][2] * m2[2][0],
      m1[1][0] * m2[0][1] + m1[1][1] * m2[1][1] + m1[1][2] * m2[2][1], 
      m1[1][0] * m2[0][2] + m1[1][1] * m2[1][2] + m1[1][2] * m2[2][2]],
      [m1[2][0] * m2[0][0] + m1[2][1] * m2[1][0] + m1[2][2] * m2[2][0],
      m1[2][0] * m2[0][1] + m1[2][1] * m2[1][1] + m1[2][2] * m2[2][1], 
      m1[2][0] * m2[0][2] + m1[2][1] * m2[1][2] + m1[2][2] * m2[2][2]]]

  @classmethod
  def translation(klass, vector):
    return klass([
      [ 1, 0, vector.x ],
      [ 0, 1, vector.y ],
      [ 0, 0, 1]
    ])

  def translate(self, vector):
    self.apply_backwards(type(self).translation(vector))

  @classmethod
  def scaling(klass, factorX, factorY = None):
    if not factorY: factorY = factorX
    return klass([
      [ factorX, 0,       0],
      [ 0,       factorY, 0],
      [ 0,       0,       1]
    ])

  def scale(self, factorX, factorY = None):
    self.apply_backwards(type(self).scaling(factorX, factorY))

  @classmethod
  def reflection(klass):
    return klass([
      [ -1, 0, 0],
      [ 0,  1, 0],
      [ 0,  0, 1]
    ])

  def reflect(self):
    self.apply_backwards(type(self).reflection)

  @classmethod
  def rotation(klass, angle):
    return klass([
      [ math.cos(-angle),  math.sin(-angle), 0 ],
      [ -math.sin(-angle), math.cos(-angle), 0 ],
      [ 0,                0,               1 ]
    ])

  def rotate(self, angle):
    self.apply_backwards(type(self).rotation(angle))

  def invert(self):
    m = self.matrix
    det = m[0][0] * (m[1][1]*m[2][2] - m[1][2]*m[2][1]) - \
          m[0][1] * (m[1][0]*m[2][2] - m[1][2]*m[2][0]) + \
          m[0][2] * (m[1][0]*m[2][1] - m[1][1]*m[2][0])
    if isclose(det, 0.):
        return None
    adj = [[(m[1][1]*m[2][2] - m[2][1]*m[1][2])/det, (m[2][1]*m[0][2] - m[0][1]*m[2][2])/det, (m[0][1]*m[1][2] - m[1][1]*m[0][2])/det],
           [(m[1][2]*m[2][0] - m[1][0]*m[2][2])/det, (m[0][0]*m[2][2] - m[0][2]*m[2][0])/det, (m[0][2]*m[1][0] - m[0][0]*m[1][2])/det],
           [(m[1][0]*m[2][1] - m[1][1]*m[2][0])/det, (m[0][1]*m[2][0] - m[0][0]*m[2][1])/det, (m[0][0]*m[1][1] - m[0][1]*m[1][0])/det]]
    self.matrix = adj

