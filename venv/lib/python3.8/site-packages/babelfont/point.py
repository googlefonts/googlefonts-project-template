from fontParts.base.point import BasePoint
from babelfont import addUnderscoreProperty


@addUnderscoreProperty("x")
@addUnderscoreProperty("y")
@addUnderscoreProperty("type")
@addUnderscoreProperty("smooth")
@addUnderscoreProperty("contour")
@addUnderscoreProperty("name")
@addUnderscoreProperty("identifier")
class Point(BasePoint):
    pass
