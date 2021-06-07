from fontParts.base.anchor import BaseAnchor
from babelfont import addUnderscoreProperty


@addUnderscoreProperty("name")
@addUnderscoreProperty("glyph")
@addUnderscoreProperty("color")
@addUnderscoreProperty("x")
@addUnderscoreProperty("y")
class Anchor(BaseAnchor):
    def __init__(self, **kwargs):
        self.x = 0
        self.y = 0
        super().__init__(**kwargs)

    def _get_identifier(self):
        return self.name
