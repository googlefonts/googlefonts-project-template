import unittest
from fontParts.base.deprecated import RemovedError


class TestDeprecated(unittest.TestCase):

    # ----
    # Font
    # ----

    def getFont_glyphs(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newGlyph(name)
        return font

    def test_font_removed_getParent(self):
        font, _ = self.objectGenerator("font")
        with self.assertRaises(RemovedError):
            font.getParent()

    def test_font_removed_generateGlyph(self):
        font, _ = self.objectGenerator("font")
        with self.assertRaises(RemovedError):
            font.generateGlyph()

    def test_font_removed_compileGlyph(self):
        font, _ = self.objectGenerator("font")
        with self.assertRaises(RemovedError):
            font.compileGlyph()

    def test_font_removed_getGlyphNameToFileNameFunc(self):
        font, _ = self.objectGenerator("font")
        with self.assertRaises(RemovedError):
            font.getGlyphNameToFileNameFunc()

    def test_font_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        font, _ = self.objectGenerator("font")
        with self.assertWarnsRegex(DeprecationWarning, "Font.changed()"):
            font.update()

    def test_font_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        font, _ = self.objectGenerator("font")
        with self.assertWarnsRegex(DeprecationWarning, "Font.changed()"):
            font.setChanged()

    def test_font_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        with self.assertRaises(RemovedError):
            font.setParent(font)

    def test_font_deprecated__fileName(self):
        font, _ = self.objectGenerator("font")
        with self.assertWarnsRegex(DeprecationWarning, "fileName"):
            font._get_fileName()
        self.assertEqual(font._get_fileName(), font.path)

    def test_font_deprecated_fileName(self):
        font, _ = self.objectGenerator("font")
        with self.assertWarnsRegex(DeprecationWarning, "fileName"):
            font.fileName
        self.assertEqual(font.fileName, font.path)

    def test_font_deprecated_getWidth(self):
        font, _ = self.objectGenerator("font")
        glyph = font.newGlyph("Test")
        glyph.width = 200
        with self.assertWarnsRegex(DeprecationWarning, "Font.getWidth()"):
            font.getWidth("Test")
        self.assertEqual(font.getWidth("Test"), font["Test"].width)

    def test_font_deprecated_getGlyph(self):
        font, _ = self.objectGenerator("font")
        font.newGlyph("Test")
        with self.assertWarnsRegex(DeprecationWarning, "Font.getGlyph()"):
            font.getGlyph("Test")
        self.assertEqual(font.getGlyph("Test"), font["Test"])

    def test_font_deprecated__get_selection(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        with self.assertWarnsRegex(DeprecationWarning, "Font.selectedGlyphNames"):
            font._get_selection()
        self.assertEqual(font._get_selection(), font.selectedGlyphNames)

    def test_font_deprecated__set_selection(self):
        font1 = self.getFont_glyphs()
        font2 = self.getFont_glyphs()
        with self.assertWarnsRegex(DeprecationWarning, "Font.selectedGlyphNames"):
            font1._set_selection(["A", "B"])
        font2.selectedGlyphNames = ["A", "B"]
        self.assertEqual(font1.selectedGlyphNames, font2.selectedGlyphNames)

    def test_font_deprecated_selection_set(self):
        font1 = self.getFont_glyphs()
        font2 = self.getFont_glyphs()
        with self.assertWarnsRegex(DeprecationWarning, "Font.selectedGlyphNames"):
            font1.selection = ["A", "B"]
        font2.selectedGlyphNames = ["A", "B"]
        self.assertEqual(font1.selectedGlyphNames, font2.selectedGlyphNames)

    def test_font_deprecated_selection_get(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        with self.assertWarnsRegex(DeprecationWarning, "Font.selectedGlyphNames"):
            font.selection
        self.assertEqual(font.selection, font.selectedGlyphNames)

    # ------
    # Anchor
    # ------

    def getAnchor(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph.appendAnchor("anchor 0", (10, 20))
        return glyph.anchors[0]

    def test_anchor_deprecated__generateIdentifer(self):
        anchor, _ = self.objectGenerator("anchor")
        with self.assertWarnsRegex(DeprecationWarning, "Anchor._generateIdentifier()"):
            anchor._generateIdentifier()
        self.assertEqual(
            anchor._generateIdentifier(),
            anchor._getIdentifier()
        )

    def test_anchor_deprecated_generateIdentifer(self):
        anchor, _ = self.objectGenerator("anchor")
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.generateIdentifier()"):
            anchor.generateIdentifier()
        self.assertEqual(
            anchor.generateIdentifier(),
            anchor.getIdentifier()
        )

    def test_anchor_deprecated_getParent(self):
        anchor = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.getParent()"):
            anchor.getParent()
        self.assertEqual(
            anchor.getParent(),
            anchor.glyph
        )

    def test_anchor_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        anchor, _ = self.objectGenerator("anchor")
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.changed()"):
            anchor.update()

    def test_anchor_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        anchor, _ = self.objectGenerator("anchor")
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.changed()"):
            anchor.setChanged()

    def test_anchor_removed_setParent(self):
        anchor = self.getAnchor()
        glyph = anchor.glyph
        with self.assertRaises(RemovedError):
            anchor.setParent(glyph)

    def test_anchor_removed_draw(self):
        anchor = self.getAnchor()
        pen = anchor.glyph.getPen()
        with self.assertRaises(RemovedError):
            anchor.draw(pen)

    def test_anchor_removed_drawPoints(self):
        anchor = self.getAnchor()
        pen = anchor.glyph.getPen()
        with self.assertRaises(RemovedError):
            anchor.drawPoints(pen)

    def test_anchor_deprecated_move(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.move()"):
            anchor1.move((0, 20))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.moveBy((0, 20))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_translate(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.translate()"):
            anchor1.translate((0, 20))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.moveBy((0, 20))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_scale_no_center(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.scale()"):
            anchor1.scale((-2))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.scaleBy((-2))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_scale_center(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.scale()"):
            anchor1.scale((-2, 3), center=(1, 2))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_rotate_no_offset(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.rotate()"):
            anchor1.rotate(45)
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.rotateBy(45)
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_rotate_offset(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.rotate()"):
            anchor1.rotate(45, offset=(1, 2))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.rotateBy(45, origin=(1, 2))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_transform(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.transform()"):
            anchor1.transform((2, 0, 0, 3, -3, 2))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_skew_no_offset_one_value(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.skew()"):
            anchor1.skew(100)
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.skewBy(100)
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_skew_no_offset_two_values(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.skew()"):
            anchor1.skew((100, 200))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.skewBy((100, 200))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_skew_offset_one_value(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.skew()"):
            anchor1.skew(100, offset=(1, 2))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.skewBy(100, origin=(1, 2))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    def test_anchor_deprecated_skew_offset_two_values(self):
        anchor1 = self.getAnchor()
        anchor2 = self.getAnchor()
        with self.assertWarnsRegex(DeprecationWarning, "Anchor.skew()"):
            anchor1.skew((100, 200), offset=(1, 2))
        self.assertNotEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))
        anchor2.skewBy((100, 200), origin=(1, 2))
        self.assertEqual((anchor1.x, anchor1.y), (anchor2.x, anchor2.y))

    # -----
    # Layer
    # -----

    def test_layer_deprecated_getParent(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newLayer("layer " + name)
        layer = font.layers[0]
        with self.assertWarnsRegex(DeprecationWarning, "Layer.font"):
            layer.getParent()
        self.assertEqual(layer.getParent(), layer.font)

    def test_layer_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        layer, _ = self.objectGenerator("layer")
        with self.assertWarnsRegex(DeprecationWarning, "Layer.changed()"):
            layer.update()

    def test_layer_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        layer, _ = self.objectGenerator("layer")
        with self.assertWarnsRegex(DeprecationWarning, "Layer.changed()"):
            layer.setChanged()

    def test_layer_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newLayer("layer " + name)
        layer = font.layers[0]
        with self.assertRaises(RemovedError):
            layer.setParent(font)

    # --------
    # Features
    # --------

    def test_features_deprecated_getParent(self):
        font, _ = self.objectGenerator("font")
        features = font.features
        features.text = "# Test"
        with self.assertWarnsRegex(DeprecationWarning, "Features.font"):
            features.getParent()
        self.assertEqual(features.getParent(), features.font)

    def test_features_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        features, _ = self.objectGenerator("features")
        with self.assertWarnsRegex(DeprecationWarning, "Features.changed()"):
            features.update()

    def test_features_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        features, _ = self.objectGenerator("features")
        with self.assertWarnsRegex(DeprecationWarning, "Features.changed()"):
            features.setChanged()

    def test_feature_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        features = font.features
        features.text = "# Test"
        with self.assertRaises(RemovedError):
            features.setParent(font)

    def test_feature_removed_round(self):
        feature, _ = self.objectGenerator("features")
        with self.assertRaises(RemovedError):
            feature.round()

    # -----
    # Image
    # -----

    def getImage_glyph(self):
        from fontParts.test.test_image import testImageData
        glyph, _ = self.objectGenerator("glyph")
        glyph.addImage(data=testImageData)
        image = glyph.image
        return image

    def test_image_deprecated_getParent(self):
        image = self.getImage_glyph()
        with self.assertWarnsRegex(DeprecationWarning, "Image.glyph"):
            image.getParent()
        self.assertEqual(image.getParent(), image.glyph)

    def test_image_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        image, _ = self.objectGenerator("image")
        with self.assertWarnsRegex(DeprecationWarning, "Image.changed()"):
            image.update()

    def test_image_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        image, _ = self.objectGenerator("image")
        with self.assertWarnsRegex(DeprecationWarning, "Image.changed()"):
            image.setChanged()

    def test_image_removed_setParent(self):
        glyph, _ = self.objectGenerator("glyph")
        image = self.getImage_glyph()
        with self.assertRaises(RemovedError):
            image.setParent(glyph)

    # ----
    # Info
    # ----

    def test_info_deprecated_getParent(self):
        font, _ = self.objectGenerator("font")
        info = font.info
        info.unitsPerEm = 1000
        with self.assertWarnsRegex(DeprecationWarning, "Info.font"):
            info.getParent()
        self.assertEqual(info.getParent(), info.font)

    def test_info_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        info, _ = self.objectGenerator("info")
        with self.assertWarnsRegex(DeprecationWarning, "Info.changed()"):
            info.update()

    def test_info_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        info, _ = self.objectGenerator("info")
        with self.assertWarnsRegex(DeprecationWarning, "Info.changed()"):
            info.setChanged()

    def test_info_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        info, _ = self.objectGenerator("info")
        info.unitsPerEm = 1000
        with self.assertRaises(RemovedError):
            info.setParent(font)

    # -------
    # Kerning
    # -------

    def getKerning_generic(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        groups["public.kern1.X"] = ["A", "B", "C"]
        groups["public.kern2.X"] = ["A", "B", "C"]
        kerning = font.kerning
        kerning.update({
            ("public.kern1.X", "public.kern2.X"): 100,
            ("B", "public.kern2.X"): 101,
            ("public.kern1.X", "B"): 102,
            ("A", "A"): 103,
        })
        return kerning

    def test_kerning_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        kerning, _ = self.objectGenerator("kerning")
        with self.assertRaises(RemovedError):
            kerning.setParent(font)

    def test_kerning_removed_swapNames(self):
        kerning = self.getKerning_generic()
        swap = {"B": "C"}
        with self.assertRaises(RemovedError):
            kerning.swapNames(swap)

    def test_kerning_removed_getLeft(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.getLeft("B")

    def test_kerning_removed_getRight(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.getRight("B")

    def test_kerning_removed_getExtremes(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.getExtremes()

    def test_kerning_removed_add(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.add(10)

    def test_kerning_removed_minimize(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.minimize()

    def test_kerning_removed_importAFM(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.importAFM("fake/path")

    def test_kerning_removed_getAverage(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.getAverage()

    def test_kerning_removed_combine(self):
        kerning = self.getKerning_generic()
        one = {("A", "v"): -10}
        two = {("v", "A"): -10}
        with self.assertRaises(RemovedError):
            kerning.combine([one, two])

    def test_kerning_removed_eliminate(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.eliminate(leftGlyphsToEliminate=["A"])

    def test_kerning_removed_occurrenceCount(self):
        kerning = self.getKerning_generic()
        with self.assertRaises(RemovedError):
            kerning.occurrenceCount(["A"])

    def test_kerning_removed_implodeClasses(self):
        kerning = self.getKerning_generic()
        classes = {"group": ["a", "v"]}
        with self.assertRaises(RemovedError):
            kerning.implodeClasses(leftClassDict=classes)

    def test_kerning_removed_explodeClasses(self):
        kerning = self.getKerning_generic()
        classes = {"group": ["a", "v"]}
        with self.assertRaises(RemovedError):
            kerning.explodeClasses(leftClassDict=classes)

    def test_kerning_removed_setChanged(self):
        kerning = self.getKerning_generic()
        # As changed() is defined by the environment, only test if a Warning is issued.
        with self.assertWarnsRegex(DeprecationWarning, "Kerning.changed()"):
            kerning.setChanged()

    def test_kerning_removed_getParent(self):
        kerning = self.getKerning_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Kerning.font"):
            kerning.getParent()
        self.assertEqual(kerning.getParent(), kerning.font)

    # ------
    # Groups
    # ------

    def test_groups_deprecated_getParent(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        groups.update({
            "group 1": ["A", "B", "C"],
            "group 2": ["x", "y", "z"],
            "group 3": [],
            "group 4": ["A"]
        })
        with self.assertWarnsRegex(DeprecationWarning, "Groups.font"):
            groups.getParent()
        self.assertEqual(groups.getParent(), groups.font)

    def test_groups_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        groups, _ = self.objectGenerator("groups")
        with self.assertWarnsRegex(DeprecationWarning, "Groups.changed()"):
            groups.setChanged()

    def test_groups_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        groups, _ = self.objectGenerator("groups")
        groups.update({
            "group 1": ["A", "B", "C"],
            "group 2": ["x", "y", "z"],
            "group 3": [],
            "group 4": ["A"]
        })
        with self.assertRaises(RemovedError):
            groups.setParent(font)

    # ---
    # Lib
    # ---

    def test_lib_deprecated_getParent_font(self):
        font, _ = self.objectGenerator("font")
        lib = font.lib
        lib.update({
            "key 1": ["A", "B", "C"],
            "key 2": "x",
            "key 3": [],
            "key 4": 20
        })
        with self.assertWarnsRegex(DeprecationWarning, "Lib.font"):
            lib.getParent()
        self.assertEqual(lib.getParent(), lib.font)

    def test_lib_deprecated_getParent_glyph(self):
        font, _ = self.objectGenerator("font")
        glyph = font.newGlyph("Test")
        lib = glyph.lib
        lib.update({
            "key 1": ["A", "B", "C"],
            "key 2": "x",
            "key 3": [],
            "key 4": 20
        })
        with self.assertWarnsRegex(DeprecationWarning, "Lib.glyph"):
            lib.getParent()
        self.assertEqual(lib.getParent(), lib.glyph)

    def test_lib_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        lib, _ = self.objectGenerator("lib")
        with self.assertWarnsRegex(DeprecationWarning, "Lib.changed()"):
            lib.setChanged()

    def test_lib_removed_setParent_font(self):
        font, _ = self.objectGenerator("font")
        lib, _ = self.objectGenerator("lib")
        lib.update({
            "key 1": ["A", "B", "C"],
            "key 2": "x",
            "key 3": [],
            "key 4": 20
        })
        with self.assertRaises(RemovedError):
            lib.setParent(font)

    def test_lib_removed_setParent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        lib, _ = self.objectGenerator("lib")
        lib.update({
            "key 1": ["A", "B", "C"],
            "key 2": "x",
            "key 3": [],
            "key 4": 20
        })
        with self.assertRaises(RemovedError):
            lib.setParent(glyph)

    # ---------
    # Guideline
    # ---------

    def getGuideline_generic(self):
        guideline, _ = self.objectGenerator("guideline")
        guideline.x = 1
        guideline.y = 2
        guideline.angle = 90
        return guideline

    def getGuideline_transform(self):
        guideline = self.getGuideline_generic()
        guideline.angle = 45.0
        return guideline

    def test_guideline_deprecated__generateIdentifer(self):
        guideline = self.getGuideline_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline._getIdentifier()"):
            guideline._generateIdentifier()
        self.assertEqual(guideline._generateIdentifier(), guideline._getIdentifier())

    def test_guideline_deprecated_generateIdentifer(self):
        guideline = self.getGuideline_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.getIdentifier()"):
            guideline.generateIdentifier()
        self.assertEqual(guideline.generateIdentifier(), guideline.getIdentifier())

    def test_guideline_deprecated_getParent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        guideline = self.getGuideline_generic()
        guideline.glyph = glyph
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.glyph"):
            guideline.getParent()
        self.assertEqual(guideline.getParent(), guideline.glyph)

    def test_guideline_deprecated_getParent_font(self):
        font, _ = self.objectGenerator("font")
        guideline = self.getGuideline_generic()
        guideline.font = font
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.font"):
            guideline.getParent()
        self.assertEqual(guideline.getParent(), guideline.font)

    def test_guideline_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        guideline, _ = self.objectGenerator("guideline")
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.changed()"):
            guideline.update()

    def test_guideline_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        guideline, _ = self.objectGenerator("guideline")
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.changed()"):
            guideline.setChanged()

    def test_guideline_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        guideline = self.getGuideline_generic()
        with self.assertRaises(RemovedError):
            guideline.setParent(font)

    def test_guideline_deprecated_move(self):
        guideline1, _ = self.objectGenerator("guideline")
        guideline2, _ = self.objectGenerator("guideline")
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.move()"):
            guideline1.move((0, 20))
        guideline2.moveBy((0, 20))
        self.assertEqual(guideline1.y, guideline2.y)

    def test_guideline_deprecated_translate(self):
        guideline1, _ = self.objectGenerator("guideline")
        guideline2, _ = self.objectGenerator("guideline")
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.translate()"):
            guideline1.translate((0, 20))
        guideline2.moveBy((0, 20))
        self.assertEqual(guideline1.y, guideline2.y)

    def test_guideline_deprecated_scale_no_center(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.scale()"):
            guideline.scale((-2))
        self.assertEqual(guideline.x, -2)
        self.assertEqual(guideline.y, -4)
        self.assertAlmostEqual(guideline.angle, 225.000, places=3)

    def test_guideline_deprecated_scale_center(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.scale()"):
            guideline.scale((-2, 3), center=(1, 2))
        self.assertEqual(guideline.x, 1)
        self.assertEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 123.690, places=3)

    def test_guideline_deprecated_rotate_no_offset(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.rotate()"):
            guideline.rotate(45)
        self.assertAlmostEqual(guideline.x, -0.707, places=3)
        self.assertAlmostEqual(guideline.y, 2.121, places=3)
        self.assertAlmostEqual(guideline.angle, 0.000, places=3)

    def test_guideline_deprecated_rotate_offset(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.rotate()"):
            guideline.rotate(45, offset=(1, 2))
        self.assertAlmostEqual(guideline.x, 1)
        self.assertAlmostEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 0.000, places=3)

    def test_guideline_deprecated_transform(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.transform()"):
            guideline.transform((2, 0, 0, 3, -3, 2))
        self.assertEqual(guideline.x, -1)
        self.assertEqual(guideline.y, 8)
        self.assertAlmostEqual(guideline.angle, 56.310, places=3)

    def test_guideline_deprecated_skew_no_offset_one_value(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.skew()"):
            guideline.skew(100)
        self.assertAlmostEqual(guideline.x, -10.343, places=3)
        self.assertEqual(guideline.y, 2.0)
        self.assertAlmostEqual(guideline.angle, 8.525, places=3)

    def test_guideline_deprecated_skew_no_offset_two_values(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.skew()"):
            guideline.skew((100, 200))
        self.assertAlmostEqual(guideline.x, -10.343, places=3)
        self.assertAlmostEqual(guideline.y, 2.364, places=3)
        self.assertAlmostEqual(guideline.angle, 5.446, places=3)

    def test_guideline_deprecated_skew_offset_one_value(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.skew()"):
            guideline.skew(100, offset=(1, 2))
        self.assertEqual(guideline.x, 1)
        self.assertEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 8.525, places=3)

    def test_guideline_deprecated_skew_offset_two_values(self):
        guideline = self.getGuideline_transform()
        with self.assertWarnsRegex(DeprecationWarning, "Guideline.skew()"):
            guideline.skew((100, 200), offset=(1, 2))
        self.assertEqual(guideline.x, 1)
        self.assertEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 5.446, places=3)

    # -----
    # Glyph
    # -----

    def getGlyph_generic(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph.name = "Test Glyph 1"
        glyph.unicode = int(ord("X"))
        glyph.width = 250
        glyph.height = 750
        pen = glyph.getPen()
        pen.moveTo((100, -10))
        pen.lineTo((100, 100))
        pen.lineTo((200, 100))
        pen.lineTo((200, 0))
        pen.closePath()
        pen.moveTo((110, 10))
        pen.lineTo((110, 90))
        pen.lineTo((190, 90))
        pen.lineTo((190, 10))
        pen.closePath()
        glyph.appendAnchor("Test Anchor 1", (1, 2))
        glyph.appendAnchor("Test Anchor 2", (3, 4))
        glyph.appendGuideline((1, 2), 0, "Test Guideline 1")
        glyph.appendGuideline((3, 4), 90, "Test Guideline 2")
        return glyph

    def test_glyph_removed_center(self):
        glyph = self.getGlyph_generic()
        with self.assertRaisesRegex(RemovedError, "center()"):
            glyph.center()

    def test_glyph_removed_clearVGuides(self):
        glyph = self.getGlyph_generic()
        with self.assertRaisesRegex(RemovedError, "clearGuidelines()"):
            glyph.clearVGuides()

    def test_glyph_removed_clearHGuides(self):
        glyph = self.getGlyph_generic()
        with self.assertRaisesRegex(RemovedError, "clearGuidelines()"):
            glyph.clearHGuides()

    def test_glyph_removed_setParent(self):
        font, _ = self.objectGenerator("font")
        glyph = self.getGlyph_generic()
        with self.assertRaisesRegex(RemovedError, "setParent()"):
            glyph.setParent(font)

    def test_glyph_deprecated_get_mark(self):
        glyph = self.getGlyph_generic()
        glyph.markColor = (1, 0, 0, 1)
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.markColor"):
            glyph._get_mark()
        self.assertEqual(glyph._get_mark(), glyph.markColor)

    def test_glyph_deprecated_set_mark(self):
        glyph = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.markColor"):
            glyph._set_mark((1, 0, 0, 1))
        self.assertEqual((1, 0, 0, 1), glyph.markColor)

    def test_glyph_deprecated_mark(self):
        glyph = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.markColor"):
            glyph.mark = (1, 0, 0, 1)
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.markColor"):
            mark = glyph.mark
        self.assertEqual((1, 0, 0, 1), mark)

    def test_glyph_deprecated__get_box(self):
        glyph = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.bounds"):
            glyph._get_box()
        self.assertEqual(glyph._get_box(), glyph.bounds)

    def test_glyph_deprecated_box(self):
        glyph = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.bounds"):
            box = glyph.box
        self.assertEqual(box, (100, -10, 200, 100))

    def test_glyph_deprecated_getAnchors(self):
        glyph = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.anchors"):
            anchors = glyph.getAnchors()
        self.assertEqual(anchors, glyph.anchors)

    def test_glyph_deprecated_getComponents(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.components"):
            components = glyph.getComponents()
        self.assertEqual(components, glyph.components)

    def test_glyph_deprecated_getParent(self):
        font, _ = self.objectGenerator("font")
        layer = font.layers[0]
        glyph = layer.newGlyph("A")
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.font"):
            parent = glyph.getParent()
        self.assertEqual(parent, glyph.font)

    def test_glyph_deprecated_writeGlyphToString(self):
        glyph = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.dumpToGLIF()"):
            data = glyph.writeGlyphToString()
        self.assertEqual(data, glyph.dumpToGLIF())

    def test_glyph_deprecated_readGlyphToString(self):
        glyph = self.getGlyph_generic()
        glyph2, _ = self.objectGenerator("glyph")
        data = glyph.dumpToGLIF()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.loadFromGLIF()"):
            glyph2.readGlyphFromString(data)
        self.assertEqual(glyph.bounds, glyph2.bounds)
        self.assertEqual(len(glyph), len(glyph2))

    def test_glyph_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        glyph, _ = self.objectGenerator("glyph")
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.changed()"):
            glyph.update()

    def test_glyph_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        glyph, _ = self.objectGenerator("glyph")
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.changed()"):
            glyph.setChanged()

    def test_glyph_deprecated_move(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.move()"):
            glyph1.move((0, 20))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.moveBy((0, 20))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_translate(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.translate()"):
            glyph1.translate((0, 20))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.moveBy((0, 20))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_scale_no_center(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.scale()"):
            glyph1.scale((-2))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.scaleBy((-2))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_scale_center(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.scale()"):
            glyph1.scale((-2, 3), center=(1, 2))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_rotate_no_offset(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.rotate()"):
            glyph1.rotate(45)
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.rotateBy(45)
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_rotate_offset(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.rotate()"):
            glyph1.rotate(45, offset=(1, 2))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.rotateBy(45, origin=(1, 2))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_transform(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.transform()"):
            glyph1.transform((2, 0, 0, 3, -3, 2))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_skew_no_offset_one_value(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.skew()"):
            glyph1.skew(100)
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.skewBy(100)
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_skew_no_offset_two_values(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.skew()"):
            glyph1.skew((100, 200))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.skewBy((100, 200))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_skew_offset_one_value(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.skew()"):
            glyph1.skew(100, offset=(1, 2))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.skewBy(100, origin=(1, 2))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    def test_glyph_deprecated_skew_offset_two_values(self):
        glyph1 = self.getGlyph_generic()
        glyph2 = self.getGlyph_generic()
        with self.assertWarnsRegex(DeprecationWarning, "Glyph.skew()"):
            glyph1.skew((100, 200), offset=(1, 2))
        self.assertNotEqual(glyph1.bounds, glyph2.bounds)
        glyph2.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(glyph1.bounds, glyph2.bounds)

    # -------
    # Contour
    # -------

    def getContour_bounds(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((100, 100), "line")
        contour.appendPoint((100, 0), "line")
        return contour

    def test_contour_removed_setParent(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        with self.assertRaisesRegex(RemovedError, "setParent()"):
            contour.setParent(glyph)

    def test_contour_deprecated__get_box(self):
        contour = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.bounds"):
            box = contour._get_box()
        self.assertEqual(box, contour.bounds)

    def test_contour_deprecated_box(self):
        contour = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.bounds"):
            box = contour.box
        self.assertEqual(box, contour.bounds)

    def test_contour_deprecated_reverseContour(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        self.assertEqual(contour1.clockwise, contour2.clockwise)
        with self.assertWarnsRegex(DeprecationWarning, "Contour.reverse()"):
            contour1.reverseContour()
        self.assertNotEqual(contour1.clockwise, contour2.clockwise)
        contour2.reverse()
        self.assertEqual(contour1.clockwise, contour2.clockwise)

    def test_contour_deprecated__generateIdentifer(self):
        contour, _ = self.objectGenerator("contour")
        with self.assertWarnsRegex(DeprecationWarning, "Contour._generateIdentifier()"):
            i = contour._generateIdentifier()
        self.assertEqual(i, contour._getIdentifier())

    def test_contour_deprecated_generateIdentifer(self):
        contour, _ = self.objectGenerator("contour")
        with self.assertWarnsRegex(DeprecationWarning, "Contour.generateIdentifier()"):
            i = contour.generateIdentifier()
        self.assertEqual(i, contour.getIdentifier())

    def test_contour_deprecated__generateIdentiferforPoint(self):
        contour = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning,
                                   "Contour._generateIdentifierforPoint()"):
            i = contour._generateIdentifierforPoint(contour[0][0])
        self.assertEqual(i, contour._getIdentifierforPoint(contour[0][0]))

    def test_contour_deprecated_generateIdentiferForPoint(self):
        contour = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning,
                                   "Contour.generateIdentifierforPoint()"):
            i = contour.generateIdentifierforPoint(contour[0][0])
        self.assertEqual(i, contour.getIdentifierForPoint(contour[0][0]))

    def test_contour_deprecated_getParent(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        with self.assertWarnsRegex(DeprecationWarning, "Contour.glyph"):
            p = contour.getParent()
        self.assertEqual(p, contour.glyph)

    def test_contour_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        contour, _ = self.objectGenerator("contour")
        with self.assertWarnsRegex(DeprecationWarning, "Contour.changed()"):
            contour.update()

    def test_contour_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        contour, _ = self.objectGenerator("contour")
        with self.assertWarnsRegex(DeprecationWarning, "Contour.changed()"):
            contour.setChanged()

    def test_contour_deprecated_move(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.move()"):
            contour1.move((0, 20))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.moveBy((0, 20))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_translate(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.translate()"):
            contour1.translate((0, 20))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.moveBy((0, 20))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_scale_no_center(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.scale()"):
            contour1.scale((-2))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.scaleBy((-2))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_scale_center(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.scale()"):
            contour1.scale((-2, 3), center=(1, 2))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_rotate_no_offset(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.rotate()"):
            contour1.rotate(45)
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.rotateBy(45)
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_rotate_offset(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.rotate()"):
            contour1.rotate(45, offset=(1, 2))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.rotateBy(45, origin=(1, 2))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_transform(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.transform()"):
            contour1.transform((2, 0, 0, 3, -3, 2))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_skew_no_offset_one_value(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.skew()"):
            contour1.skew(100)
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.skewBy(100)
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_skew_no_offset_two_values(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.skew()"):
            contour1.skew((100, 200))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.skewBy((100, 200))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_skew_offset_one_value(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.skew()"):
            contour1.skew(100, offset=(1, 2))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.skewBy(100, origin=(1, 2))
        self.assertEqual(contour1.bounds, contour2.bounds)

    def test_contour_deprecated_skew_offset_two_values(self):
        contour1 = self.getContour_bounds()
        contour2 = self.getContour_bounds()
        with self.assertWarnsRegex(DeprecationWarning, "Contour.skew()"):
            contour1.skew((100, 200), offset=(1, 2))
        self.assertNotEqual(contour1.bounds, contour2.bounds)
        contour2.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(contour1.bounds, contour2.bounds)

    # -------
    # Segment
    # -------

    def getSegment(self):
        contour, unrequested = self.objectGenerator("contour")
        unrequested.append(contour)
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        segment = contour[1]
        return segment

    def test_segment_removed_insertPoint(self):
        segment = self.getSegment()
        with self.assertRaisesRegex(RemovedError, "insertPoint()"):
            segment.insertPoint(None)

    def test_segment_removed_removePoint(self):
        segment = self.getSegment()
        with self.assertRaisesRegex(RemovedError, "removePoint()"):
            segment.removePoint(None)

    def test_segment_removed_setParent(self):
        segment = self.getSegment()
        with self.assertRaisesRegex(RemovedError, "setParent()"):
            segment.setParent(None)

    def test_segment_deprecated_getParent(self):
        segment = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.contour"):
            c = segment.getParent()
        self.assertEqual(c, segment.contour)

    def test_segment_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        segment = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.changed()"):
            segment.update()

    def test_segment_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        segment = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.changed()"):
            segment.setChanged()

    def test_segment_deprecated_move(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.move()"):
            segment1.move((0, 20))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.moveBy((0, 20))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_translate(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.translate()"):
            segment1.translate((0, 20))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.moveBy((0, 20))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_scale_no_center(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.scale()"):
            segment1.scale((-2))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.scaleBy((-2))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_scale_center(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.scale()"):
            segment1.scale((-2, 3), center=(1, 2))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.scaleBy((-2, 3), origin=(1, 2))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_rotate_no_offset(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.rotate()"):
            segment1.rotate(45)
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.rotateBy(45)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_rotate_offset(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.rotate()"):
            segment1.rotate(45, offset=(1, 2))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.rotateBy(45, origin=(1, 2))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_transform(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.transform()"):
            segment1.transform((2, 0, 0, 3, -3, 2))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.transformBy((2, 0, 0, 3, -3, 2))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_skew_no_offset_one_value(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.skew()"):
            segment1.skew(100)
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.skewBy(100)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_skew_no_offset_two_values(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.skew()"):
            segment1.skew((100, 200))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.skewBy((100, 200))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_skew_offset_one_value(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.skew()"):
            segment1.skew(100, offset=(1, 2))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.skewBy(100, origin=(1, 2))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    def test_segment_deprecated_skew_offset_two_values(self):
        segment1 = self.getSegment()
        segment2 = self.getSegment()
        with self.assertWarnsRegex(DeprecationWarning, "Segment.skew()"):
            segment1.skew((100, 200), offset=(1, 2))
        coordinates1 = tuple((point.x, point.y) for point in segment1.points)
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertNotEqual(coordinates1, coordinates2)
        segment2.skewBy((100, 200), origin=(1, 2))
        coordinates2 = tuple((point.x, point.y) for point in segment2.points)
        self.assertEqual(coordinates1, coordinates2)

    # ---------
    # Component
    # ---------

    def getComponent(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("A")
        pen = glyph.getPen()
        pen.moveTo((0, 0))
        pen.lineTo((0, 100))
        pen.lineTo((100, 100))
        pen.lineTo((100, 0))
        pen.closePath()
        for i, point in enumerate(glyph[0].points):
            point.name = "point %d" % i
        glyph = layer.newGlyph("B")
        component = glyph.appendComponent("A")
        component.transformation = (1, 2, 3, 4, 5, 6)
        return component

    def test_component_removed_setParent(self):
        component = self.getComponent()
        with self.assertRaisesRegex(RemovedError, "setParent()"):
            component.setParent(None)

    def test_component_deprecated__get_box(self):
        component = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.bounds"):
            box = component._get_box()
        self.assertEqual(box, component.bounds)

    def test_component_deprecated_box(self):
        component = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.bounds"):
            box = component.box
        self.assertEqual(box, component.bounds)

    def test_component_deprecated__generateIdentifier(self):
        component = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component._getIdentifier()"):
            i = component._generateIdentifier()
        self.assertEqual(i, component._getIdentifier())

    def test_component_deprecated_generateIdentifier(self):
        component = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.getIdentifier()"):
            i = component.generateIdentifier()
        self.assertEqual(i, component.getIdentifier())

    def test_component_deprecated_getParent(self):
        component = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.glyph"):
            p = component.getParent()
        self.assertEqual(p, component.glyph)

    def test_component_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        component = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.changed()"):
            component.update()

    def test_component_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        component = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.changed()"):
            component.setChanged()

    def test_component_deprecated_move(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.move()"):
            component1.move((0, 20))
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.moveBy((0, 20))
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_translate(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.translate()"):
            component1.translate((0, 20))
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.moveBy((0, 20))
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_rotate_no_offset(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.rotate()"):
            component1.rotate(45)
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.rotateBy(45)
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_rotate_offset(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.rotate()"):
            component1.rotate(45, offset=(1, 2))
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.rotateBy(45, origin=(1, 2))
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_transform(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.transform()"):
            component1.transform((2, 0, 0, 3, -3, 2))
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_skew_no_offset_one_value(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.skew()"):
            component1.skew(100)
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.skewBy(100)
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_skew_no_offset_two_values(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.skew()"):
            component1.skew((100, 200))
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.skewBy((100, 200))
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_skew_offset_one_value(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.skew()"):
            component1.skew(100, offset=(1, 2))
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.skewBy(100, origin=(1, 2))
        self.assertEqual(component1.bounds, component2.bounds)

    def test_component_deprecated_skew_offset_two_values(self):
        component1 = self.getComponent()
        component2 = self.getComponent()
        with self.assertWarnsRegex(DeprecationWarning, "Component.skew()"):
            component1.skew((100, 200), offset=(1, 2))
        self.assertNotEqual(component1.bounds, component2.bounds)
        component2.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(component1.bounds, component2.bounds)

    # -----
    # Point
    # -----

    def getPoint(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        point = contour.points[1]
        point.smooth = True
        return point

    def test_point_removed_select(self):
        point = self.getPoint()
        with self.assertRaisesRegex(RemovedError, "Point.select"):
            point.select()

    def test_point_removed_setParent(self):
        point = self.getPoint()
        with self.assertRaisesRegex(RemovedError, "setParent()"):
            point.setParent(None)

    def test_point_deprecated__generateIdentifier(self):
        point = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point._getIdentifier()"):
            i = point._generateIdentifier()
        self.assertEqual(i, point._getIdentifier())

    def test_point_deprecated_generateIdentifier(self):
        point = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.getIdentifier()"):
            i = point.generateIdentifier()
        self.assertEqual(i, point.getIdentifier())

    def test_point_getParent(self):
        point = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.contour"):
            p = point.getParent()
        self.assertEqual(p, point.contour)

    def test_point_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        point = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.changed()"):
            point.update()

    def test_point_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        point = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.changed()"):
            point.setChanged()

    def test_point_deprecated_move(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.move()"):
            point1.move((0, 20))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.moveBy((0, 20))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_translate(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.translate()"):
            point1.translate((0, 20))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.moveBy((0, 20))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_scale_no_center(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.scale()"):
            point1.scale((-2))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.scaleBy((-2))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_scale_center(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.scale()"):
            point1.scale((-2, 3), center=(1, 2))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_rotate_no_offset(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.rotate()"):
            point1.rotate(45)
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.rotateBy(45)
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_rotate_offset(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.rotate()"):
            point1.rotate(45, offset=(1, 2))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.rotateBy(45, origin=(1, 2))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_transform(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.transform()"):
            point1.transform((2, 0, 0, 3, -3, 2))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_skew_no_offset_one_value(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.skew()"):
            point1.skew(100)
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.skewBy(100)
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_skew_no_offset_two_values(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.skew()"):
            point1.skew((100, 200))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.skewBy((100, 200))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_skew_offset_one_value(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.skew()"):
            point1.skew(100, offset=(1, 2))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.skewBy(100, origin=(1, 2))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    def test_point_deprecated_skew_offset_two_values(self):
        point1 = self.getPoint()
        point2 = self.getPoint()
        with self.assertWarnsRegex(DeprecationWarning, "Point.skew()"):
            point1.skew((100, 200), offset=(1, 2))
        self.assertNotEqual((point1.x, point1.y), (point2.x, point2.y))
        point2.skewBy((100, 200), origin=(1, 2))
        self.assertEqual((point1.x, point1.y), (point2.x, point2.y))

    # ------
    # bPoint
    # ------

    def getBPoint(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        return bPoint

    def test_bPoint_removed_select(self):
        bPoint = self.getBPoint()
        with self.assertRaisesRegex(RemovedError, "BPoint.select"):
            bPoint.select()

    def test_bPoint_removed_setParent(self):
        bPoint = self.getBPoint()
        with self.assertRaisesRegex(RemovedError, "setParent()"):
            bPoint.setParent(None)

    def test_bPoint_deprecated__generateIdentifier(self):
        bPoint = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint._getIdentifier()"):
            i = bPoint._generateIdentifier()
        self.assertEqual(i, bPoint._getIdentifier())

    def test_bPoint_deprecated_generateIdentifier(self):
        bPoint = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.getIdentifier()"):
            i = bPoint.generateIdentifier()
        self.assertEqual(i, bPoint.getIdentifier())

    def test_bPoint_getParent(self):
        bPoint = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.contour"):
            p = bPoint.getParent()
        self.assertEqual(p, bPoint.contour)

    def test_bPoint_deprecated_update(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        bPoint = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.changed()"):
            bPoint.update()

    def test_bPoint_deprecated_setChanged(self):
        # As changed() is defined by the environment, only test if a Warning is issued.
        bPoint = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.changed()"):
            bPoint.setChanged()

    def test_bPoint_deprecated_move(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.move()"):
            bPoint1.move((0, 20))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.moveBy((0, 20))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_translate(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.translate()"):
            bPoint1.translate((0, 20))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.moveBy((0, 20))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_scale_no_center(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.scale()"):
            bPoint1.scale((-2))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.scaleBy((-2))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_scale_center(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.scale()"):
            bPoint1.scale((-2, 3), center=(1, 2))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_rotate_no_offset(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.rotate()"):
            bPoint1.rotate(45)
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.rotateBy(45)
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_rotate_offset(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.rotate()"):
            bPoint1.rotate(45, offset=(1, 2))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.rotateBy(45, origin=(1, 2))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_transform(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.transform()"):
            bPoint1.transform((2, 0, 0, 3, -3, 2))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_skew_no_offset_one_value(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.skew()"):
            bPoint1.skew(100)
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.skewBy(100)
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_skew_no_offset_two_values(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.skew()"):
            bPoint1.skew((100, 200))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.skewBy((100, 200))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_skew_offset_one_value(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.skew()"):
            bPoint1.skew(100, offset=(1, 2))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.skewBy(100, origin=(1, 2))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)

    def test_bPoint_deprecated_skew_offset_two_values(self):
        bPoint1 = self.getBPoint()
        bPoint2 = self.getBPoint()
        with self.assertWarnsRegex(DeprecationWarning, "BPoint.skew()"):
            bPoint1.skew((100, 200), offset=(1, 2))
        self.assertNotEqual(bPoint1.anchor, bPoint2.anchor)
        bPoint2.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(bPoint1.anchor, bPoint2.anchor)
