from fontTools.misc.transform import Identity, Transform

import ufo2ft.util
from ufo2ft.filters import BaseFilter


class DecomposeTransformedComponentsFilter(BaseFilter):
    def filter(self, glyph):
        if not glyph.components:
            return False
        transformedComponents = []
        for component in glyph.components:
            if component.transformation[:4] != Identity[:4]:
                transformedComponents.append(component)
        if not transformedComponents:
            return False
        specificComponents = [c.baseGlyph for c in transformedComponents]
        ufo2ft.util.deepCopyContours(
            self.context.glyphSet,
            glyph,
            glyph,
            Transform(),
            specificComponents=specificComponents,
        )
        for component in transformedComponents:
            glyph.removeComponent(component)
        return True
