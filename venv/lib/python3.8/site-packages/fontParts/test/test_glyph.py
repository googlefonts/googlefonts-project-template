import unittest
import collections
from fontParts.base import FontPartsError
from .test_image import testImageData


class TestGlyph(unittest.TestCase):

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

    def get_generic_object(self, obj_name):
        fp_object, _ = self.objectGenerator(obj_name)
        return fp_object

    # -------
    # Parents
    # -------

    def test_get_layer(self):
        font = self.get_generic_object("font")
        layer = font.layers[0]
        glyph = layer.newGlyph("A")
        self.assertEqual(
            glyph.layer,
            layer
        )

    def test_get_layer_orphan_glyph(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(glyph.layer)

    def test_get_font(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("A")
        self.assertEqual(
            glyph.font,
            font
        )

    def test_get_font_orphan_glyph(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(glyph.font)

    # --------------
    # Identification
    # --------------

    def test_get_name(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(
            glyph.name,
            "Test Glyph 1"
        )

    def test_get_name_not_set(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(
            glyph.name
        )

    def test_set_name_valid(self):
        glyph = self.getGlyph_generic()
        name = "Test Glyph 1"  # the name is intentionally the same
        glyph.name = name
        self.assertEqual(
            glyph.name,
            name
        )

    def test_set_name_invalid(self):
        invalid_names = (
            ("", ValueError),
            ("A", ValueError),  # a glyph with this name already exists
            (3, TypeError),
            (None, TypeError)
        )
        font = self.get_generic_object("font")
        font.newGlyph("A")
        glyph = font.newGlyph("B")
        for name, err in invalid_names:
            with self.assertRaises(err):
                glyph.name = name

    def test_get_unicode(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(
            glyph.unicode,
            88
        )

    def test_get_unicode_not_set(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(
            glyph.unicode
        )

    def test_set_unicode_valid(self):
        valid_uni_values = (100, None, 0x6D, '6D')
        for value in valid_uni_values:
            glyph = self.get_generic_object("glyph")
            glyph.unicode = value
            result = int(value, 16) if isinstance(value, str) else value
            self.assertEqual(
                glyph.unicode,
                result
            )

    def test_set_unicode_value(self):
        glyph = self.get_generic_object("glyph")
        glyph.unicodes = (10, 20)
        glyph.unicode = 20
        self.assertEqual(
            glyph.unicodes,
            (20,)
        )

    def test_set_unicode_value_none(self):
        glyph = self.get_generic_object("glyph")
        glyph.unicodes = (10, 20)
        glyph.unicode = None
        self.assertEqual(
            glyph.unicodes,
            ()
        )

    def test_set_unicode_invalid(self):
        invalid_uni_values = (
            ('GG', ValueError),
            (True, TypeError),
            ([], TypeError)
        )
        glyph = self.get_generic_object("glyph")
        for value, err in invalid_uni_values:
            with self.assertRaises(err):
                glyph.unicode = value

    def test_get_unicodes(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(
            glyph.unicodes,
            (88,)
        )

    def test_get_unicodes_not_set(self):
        glyph = self.get_generic_object("glyph")
        self.assertEqual(
            glyph.unicodes,
            ()
        )

    def test_set_unicodes_valid(self):
        valid_uni_values = ([100, 200], [], (300,), ())
        for values in valid_uni_values:
            glyph = self.get_generic_object("glyph")
            glyph.unicodes = values
            self.assertEqual(
                glyph.unicodes,
                tuple(values)
            )

    def test_set_unicodes_invalid(self):
        invalid_uni_values = (
            ('GG', ValueError),
            (True, TypeError),
            (30, TypeError)
        )
        glyph = self.get_generic_object("glyph")
        for value, err in invalid_uni_values:
            with self.assertRaises(err):
                glyph.unicodes = value

    def test_set_unicodes_duplicates(self):
        glyph = self.get_generic_object("glyph")
        with self.assertRaises(ValueError):
            glyph.unicodes = (200, 110, 110)

    # -------
    # Metrics
    # -------

    # The methods are dynamically generated by test_generator()

    # Methods to test that empty glyphs have margins of None

    def test_get_leftMargin_not_set(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(
            glyph.leftMargin
        )

    def test_get_rightMargin_not_set(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(
            glyph.rightMargin
        )

    def test_get_bottomMargin_not_set(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(
            glyph.bottomMargin
        )

    def test_get_topMargin_not_set(self):
        glyph = self.get_generic_object("glyph")
        self.assertIsNone(
            glyph.topMargin
        )

    # -------
    # Queries
    # -------

    def test_get_bounds(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(
            glyph.bounds,
            (100, -10, 200, 100)
        )

    # ------
    # Layers
    # ------

    def test_get_layers(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("A")
        layers = glyph.layers
        self.assertEqual(len(layers), 1)
        self.assertEqual(
            glyph.layer.name,
            font.defaultLayerName
        )
        self.assertEqual(
            layers[0],
            glyph  # a glyph layer is really just a glyph
        )
        self.assertEqual(
            layers[0].name,
            'A'
        )

    def test_get_layers_orphan_glyph(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(
            glyph.layers,
            ()
        )

    def test_getLayer_valid(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("B")
        self.assertEqual(
            glyph.getLayer(font.defaultLayerName).name,
            'B'
        )

    def test_getLayer_valid_not_found(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("B")
        with self.assertRaises(ValueError):
            # No layer named 'layer_name' in glyph 'B'
            glyph.getLayer('layer_name')

    def test_getLayer_invalid(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("B")
        with self.assertRaises(TypeError):
            glyph.getLayer()
        with self.assertRaises(TypeError):
            glyph.getLayer(None)
        with self.assertRaises(TypeError):
            glyph.getLayer(0)
        with self.assertRaises(ValueError):
            # Layer names must be at least one character long
            glyph.getLayer('')

    def test_newLayer_valid(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("C")
        self.assertEqual(len(glyph.layers), 1)
        layer = glyph.newLayer("background")
        self.assertEqual(len(glyph.layers), 2)
        self.assertEqual(layer.name, 'C')

    def test_newLayer_valid_already_exists(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("C")
        self.assertEqual(len(glyph.layers), 1)
        glyph.newLayer("mask")
        self.assertEqual(len(glyph.layers), 2)
        glyph.newLayer("mask")  # intentional duplicate line
        self.assertEqual(len(glyph.layers), 2)

    def test_newLayer_invalid(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("C")
        with self.assertRaises(TypeError):
            glyph.newLayer()
        with self.assertRaises(TypeError):
            glyph.newLayer(0)
        with self.assertRaises(ValueError):
            # Layer names must be at least one character long
            glyph.newLayer('')

    def test_removeLayer_valid_type_string(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("D")
        self.assertEqual(len(glyph.layers), 1)
        glyph.removeLayer(font.defaultLayerName)
        self.assertEqual(len(glyph.layers), 0)

    def test_removeLayer_valid_type_glyph_layer(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("D")
        self.assertEqual(len(glyph.layers), 1)
        glyph.removeLayer(glyph.layers[0])
        self.assertEqual(len(glyph.layers), 0)

    def test_removeLayer_valid_not_found_type_string(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("D")
        with self.assertRaises(ValueError):
            # No layer named 'layer_name' in glyph 'D'
            glyph.removeLayer('layer_name')

    def test_removeLayer_invalid(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("D")
        with self.assertRaises(TypeError):
            glyph.removeLayer()
        with self.assertRaises(TypeError):
            glyph.removeLayer(0)
        with self.assertRaises(ValueError):
            # Layer names must be at least one character long
            glyph.removeLayer('')

    # ------
    # Global
    # ------

    def test_clear(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        self.assertEqual(len(glyph), 2)
        self.assertEqual(len(glyph.components), 1)
        self.assertEqual(len(glyph.anchors), 2)
        self.assertEqual(len(glyph.guidelines), 2)
        glyph.clear(contours=False, components=False, anchors=False,
                    guidelines=False, image=False)
        glyph.clear()
        self.assertEqual(len(glyph), 0)
        self.assertEqual(len(glyph.components), 0)
        self.assertEqual(len(glyph.anchors), 0)
        self.assertEqual(len(glyph.guidelines), 0)

    def test_appendGlyph(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        glyph_one.appendComponent("component 1")
        glyph_two.appendComponent("component 2")
        self.assertEqual(len(glyph_one), 2)
        self.assertEqual(len(glyph_one.components), 1)
        self.assertEqual(len(glyph_one.anchors), 2)
        self.assertEqual(len(glyph_one.guidelines), 2)
        glyph_one.appendGlyph(glyph_two)
        glyph_one.appendGlyph(glyph_two, (300, -40))
        self.assertEqual(len(glyph_one), 6)
        self.assertEqual(len(glyph_one.components), 3)
        self.assertEqual(len(glyph_one.anchors), 6)
        self.assertEqual(len(glyph_one.guidelines), 6)

    # --------
    # Contours
    # --------

    def test_get_contour_invalid(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(ValueError):
            # No contour located at index 5
            glyph[5]

    def test_appendContour_offset_valid(self):
        glyph = self.getGlyph_generic()
        contour = self.get_generic_object("contour")
        contour.insertPoint(0, position=(0, 0))
        contour.insertPoint(1, position=(100, 100))
        contour.insertPoint(2, position=(0, 100))

        self.assertEqual(len(glyph), 2)
        newcontour = glyph.appendContour(contour, (45, 50))
        self.assertEqual(len(glyph), 3)

        self.assertEqual(newcontour, glyph[-1])
        self.assertEqual(len(newcontour.points), 3)
        self.assertEqual(newcontour.points[0].x, 45)
        self.assertEqual(newcontour.points[0].y, 50)

    def test_removeContour_valid(self):
        glyph = self.getGlyph_generic()
        contour = self.get_generic_object("contour")
        glyph.appendContour(contour)
        contour1 = glyph.contours[1]
        self.assertEqual(len(glyph), 3)
        glyph.removeContour(contour1)
        self.assertEqual(len(glyph), 2)
        glyph.removeContour(0)
        self.assertEqual(len(glyph), 1)

    def test_removeContour_invalid(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(ValueError):
            # No contour located at index 5
            glyph.removeContour(5)
        with self.assertRaises(FontPartsError):
            # The contour could not be found
            glyph.removeContour(self.get_generic_object("contour"))

    def test_clearContours(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(len(glyph), 2)
        glyph.clearContours()
        self.assertEqual(len(glyph), 0)

    # ----------
    # Components
    # ----------

    # appendComponent

    def test_appendComponent_invalid_circularReference(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(FontPartsError):
            glyph.appendComponent(glyph.name)

    def test_appendComponent_valid_object(self):
        glyph = self.getGlyph_generic()
        src, _ = self.objectGenerator("component")
        src.baseGlyph = "test"
        src.transformation = (1, 2, 3, 4, 5, 6)
        src.getIdentifier()
        dst = glyph.appendComponent(component=src)
        self.assertNotEqual(src, dst)
        self.assertEqual(src.baseGlyph, dst.baseGlyph)
        self.assertEqual(src.transformation, dst.transformation)
        self.assertEqual(src.identifier, dst.identifier)

    def test_appendComponent_valid_object_baseGlyph(self):
        glyph = self.getGlyph_generic()
        src, _ = self.objectGenerator("component")
        src.baseGlyph = "assigned"
        dst = glyph.appendComponent(component=src, baseGlyph="argument")
        self.assertEqual(dst.baseGlyph, "argument")

    def test_appendComponent_valid_object_offset(self):
        glyph = self.getGlyph_generic()
        src, _ = self.objectGenerator("component")
        src.baseGlyph = "test"
        src.transformation = (1, 2, 3, 4, 5, 6)
        dst = glyph.appendComponent(component=src, offset=(-1, -2))
        self.assertEqual(dst.offset, (-1, -2))
        self.assertEqual(dst.transformation, (1, 2, 3, 4, -1, -2))

    def test_appendComponent_valid_object_scale(self):
        glyph = self.getGlyph_generic()
        src, _ = self.objectGenerator("component")
        src.baseGlyph = "test"
        src.transformation = (1, 2, 3, 4, 5, 6)
        dst = glyph.appendComponent(component=src, scale=(-1, -2))
        self.assertEqual(dst.scale, (-1, -2))
        self.assertEqual(dst.transformation, (-1, 2, 3, -2, 5, 6))

    def test_appendComponent_valid_object_conflictingIdentifier(self):
        glyph = self.getGlyph_generic()
        c = glyph.appendComponent("test")
        existingIdentifier = c.getIdentifier()
        src, _ = self.objectGenerator("component")
        src.baseGlyph = "test"
        src._setIdentifier(existingIdentifier)
        dst = glyph.appendComponent(component=src)
        self.assertNotEqual(src.identifier, dst.identifier)

    def test_appendComponent_invalid_object_circularReference(self):
        glyph = self.getGlyph_generic()
        src, _ = self.objectGenerator("component")
        src.baseGlyph = glyph.name
        with self.assertRaises(FontPartsError):
            glyph.appendComponent(glyph.name)

    # removeComponent

    def test_removeComponent_valid(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        glyph.appendComponent("component 2")
        glyph.appendComponent("component 3")
        self.assertEqual(len(glyph.components), 3)
        component = glyph.components[1]
        glyph.removeComponent(component)
        self.assertEqual(len(glyph.components), 2)
        glyph.removeComponent(0)
        self.assertEqual(len(glyph.components), 1)

    def test_removeComponent_invalid(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(ValueError):
            # No component located at index 8
            glyph.removeComponent(8)
        with self.assertRaises(FontPartsError):
            # The component could not be found
            glyph.removeComponent(self.get_generic_object("component"))

    # clearComponents

    def test_clearComponents(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        self.assertEqual(len(glyph.components), 1)
        glyph.clearComponents()
        self.assertEqual(len(glyph.components), 0)

    # -------
    # Anchors
    # -------

    # appendAnchor

    def test_appendAnchor_valid_object(self):
        glyph = self.getGlyph_generic()
        src, _ = self.objectGenerator("anchor")
        src.name = "test"
        src.position = (1, 2)
        src.color = (1, 1, 1, 1)
        src.getIdentifier()
        dst = glyph.appendAnchor(anchor=src)
        self.assertNotEqual(src, dst)
        self.assertEqual(src.name, dst.name)
        self.assertEqual(src.position, dst.position)
        self.assertEqual(src.color, dst.color)
        self.assertEqual(src.identifier, dst.identifier)

    # removeAnchor

    def test_removeAnchor_valid(self):
        glyph = self.getGlyph_generic()
        glyph.appendAnchor("base", (250, 0), (1, 0, 0, 0.5))
        anchor = glyph.anchors[1]
        self.assertEqual(len(glyph.anchors), 3)
        glyph.removeAnchor(anchor)
        self.assertEqual(len(glyph.anchors), 2)
        glyph.removeAnchor(0)
        self.assertEqual(len(glyph.anchors), 1)

    def test_removeAnchor_invalid(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(ValueError):
            # No anchor located at index 4
            glyph.removeAnchor(4)
        with self.assertRaises(FontPartsError):
            # The anchor could not be found
            glyph.removeAnchor(self.get_generic_object("anchor"))

    # clearAnchors

    def test_clearAnchors(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(len(glyph.anchors), 2)
        glyph.clearAnchors()
        self.assertEqual(len(glyph.anchors), 0)

    # ----------
    # Guidelines
    # ----------

    # appendGuideline

    def test_appendGuideline_valid_object(self):
        glyph = self.getGlyph_generic()
        src, _ = self.objectGenerator("guideline")
        src.position = (1, 2)
        src.angle = 123
        src.name = "test"
        src.color = (1, 1, 1, 1)
        src.getIdentifier()
        dst = glyph.appendGuideline(guideline=src)
        self.assertNotEqual(src, dst)
        self.assertEqual(src.position, dst.position)
        self.assertEqual(src.angle, dst.angle)
        self.assertEqual(src.name, dst.name)
        self.assertEqual(src.color, dst.color)
        self.assertEqual(src.identifier, dst.identifier)

    # removeGuideline

    def test_removeGuideline_valid(self):
        glyph = self.getGlyph_generic()
        glyph.appendGuideline((5, -10), 90, None, (1, 0, 0, 0.5))
        guideline = glyph.guidelines[1]
        self.assertEqual(len(glyph.guidelines), 3)
        glyph.removeGuideline(guideline)
        self.assertEqual(len(glyph.guidelines), 2)
        glyph.removeGuideline(0)
        self.assertEqual(len(glyph.guidelines), 1)

    def test_removeGuideline_invalid(self):
        glyph = self.getGlyph_generic()
        with self.assertRaises(ValueError):
            # No guideline located at index 6
            glyph.removeGuideline(6)
        with self.assertRaises(FontPartsError):
            # The guideline could not be found
            glyph.removeGuideline(self.get_generic_object("guideline"))

    # clearGuidelines

    def test_clearGuidelines(self):
        glyph = self.getGlyph_generic()
        self.assertEqual(len(glyph.guidelines), 2)
        glyph.clearGuidelines()
        self.assertEqual(len(glyph.guidelines), 0)

    # -----
    # Image
    # -----

    def test_addImage(self):
        font = self.get_generic_object("font")
        glyph = font.newGlyph("glyphWithImage")
        image = glyph.addImage(data=testImageData)
        self.assertEqual(
            image.data,
            testImageData
        )

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        glyph_one = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            hash(glyph_one),
            hash(glyph_one)
        )

    def test_hash_object_other(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        glyph_one.name = "Test"
        glyph_two.name = "Test"
        self.assertNotEqual(
            hash(glyph_one),
            hash(glyph_two)
        )

    def test_hash_object_self_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        a = glyph_one
        self.assertEqual(
            hash(glyph_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        a = glyph_one
        self.assertNotEqual(
            hash(glyph_two),
            hash(a)
        )

    def test_is_hashable(self):
        glyph_one = self.getGlyph_generic()
        self.assertTrue(
            isinstance(glyph_one, collections.Hashable)
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        glyph_one = self.getGlyph_generic()
        glyph_one.name = "Test"
        self.assertEqual(
            glyph_one,
            glyph_one
        )

    def test_object_not_equal_other(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )

    def test_object_not_equal_other_name_same(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        glyph_one.name = "Test"
        glyph_two.name = "Test"
        self.assertNotEqual(
            glyph_one,
            glyph_two
        )

    def test_object_equal_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        a = glyph_one
        a.name = "Other"
        self.assertEqual(
            glyph_one,
            a
        )

    def test_object_not_equal_variable_assignment(self):
        glyph_one = self.getGlyph_generic()
        glyph_two = self.getGlyph_generic()
        a = glyph_one
        self.assertNotEqual(
            glyph_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        glyph = self.getGlyph_generic()
        try:
            glyph.selected = False
        except NotImplementedError:
            return
        glyph.selected = True
        self.assertTrue(
            glyph.selected
        )

    def test_not_selected_false(self):
        glyph = self.getGlyph_generic()
        try:
            glyph.selected = False
        except NotImplementedError:
            return
        self.assertFalse(
            glyph.selected
        )

    # Contours

    def test_selectedContours_default(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        try:
            contour1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedContours,
            ()
        )

    def test_selectedContours_setSubObject(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        contour2 = glyph.contours[1]
        try:
            contour1.selected = False
        except NotImplementedError:
            return
        contour2.selected = True
        self.assertEqual(
            glyph.selectedContours,
            (contour2,)
        )

    def test_selectedContours_setFilledList(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        contour2 = glyph.contours[1]
        try:
            contour1.selected = False
        except NotImplementedError:
            return
        glyph.selectedContours = [contour1, contour2]
        self.assertEqual(
            glyph.selectedContours,
            (contour1, contour2)
        )

    def test_selectedContours_setEmptyList(self):
        glyph = self.getGlyph_generic()
        contour1 = glyph.contours[0]
        try:
            contour1.selected = True
        except NotImplementedError:
            return
        glyph.selectedContours = []
        self.assertEqual(
            glyph.selectedContours,
            ()
        )

    # Components
    def test_selectedComponents_default(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        component1 = glyph.components[0]
        try:
            component1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedComponents,
            ()
        )

    def test_selectedComponents_setSubObject(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        glyph.appendComponent("component 2")
        component1 = glyph.components[0]
        component2 = glyph.components[1]
        try:
            component1.selected = False
        except NotImplementedError:
            return
        component2.selected = True
        self.assertEqual(
            glyph.selectedComponents,
            (component2,)
        )

    def test_selectedComponents_setFilledList(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        glyph.appendComponent("component 2")
        component1 = glyph.components[0]
        component2 = glyph.components[1]
        try:
            component1.selected = False
        except NotImplementedError:
            return
        glyph.selectedComponents = [component1, component2]
        self.assertEqual(
            glyph.selectedComponents,
            (component1, component2)
        )

    def test_selectedComponents_setEmptyList(self):
        glyph = self.getGlyph_generic()
        glyph.appendComponent("component 1")
        component1 = glyph.components[0]
        try:
            component1.selected = True
        except NotImplementedError:
            return
        glyph.selectedComponents = []
        self.assertEqual(
            glyph.selectedComponents,
            ()
        )

    # Anchors

    def test_selectedAnchors_default(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        try:
            anchor1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedAnchors,
            ()
        )

    def test_selectedAnchors_setSubObject(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        anchor2 = glyph.anchors[1]
        try:
            anchor1.selected = False
        except NotImplementedError:
            return
        anchor2.selected = True
        self.assertEqual(
            glyph.selectedAnchors,
            (anchor2,)
        )

    def test_selectedAnchors_setFilledList(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        anchor2 = glyph.anchors[1]
        try:
            anchor1.selected = False
        except NotImplementedError:
            return
        glyph.selectedAnchors = [anchor1, anchor2]
        self.assertEqual(
            glyph.selectedAnchors,
            (anchor1, anchor2)
        )

    def test_selectedAnchors_setEmptyList(self):
        glyph = self.getGlyph_generic()
        anchor1 = glyph.anchors[0]
        try:
            anchor1.selected = True
        except NotImplementedError:
            return
        glyph.selectedAnchors = []
        self.assertEqual(
            glyph.selectedAnchors,
            ()
        )

    # Guidelines

    def test_selectedGuidelines_default(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            glyph.selectedGuidelines,
            ()
        )

    def test_selectedGuidelines_setSubObject(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        guideline2 = glyph.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        guideline2.selected = True
        self.assertEqual(
            glyph.selectedGuidelines,
            (guideline2,)
        )

    def test_selectedGuidelines_setFilledList(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        guideline2 = glyph.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        glyph.selectedGuidelines = [guideline1, guideline2]
        self.assertEqual(
            glyph.selectedGuidelines,
            (guideline1, guideline2)
        )

    def test_selectedGuidelines_setEmptyList(self):
        glyph = self.getGlyph_generic()
        guideline1 = glyph.guidelines[0]
        try:
            guideline1.selected = True
        except NotImplementedError:
            return
        glyph.selectedGuidelines = []
        self.assertEqual(
            glyph.selectedGuidelines,
            ()
        )

    # -------------
    # Compatibility
    # -------------

    def test_isCompatible_anchors(self):
        glyph1 = self.getGlyph_generic()
        glyph1.clearAnchors()
        glyph1.appendAnchor("a", (0, 0))
        glyph1.appendAnchor("b", (0, 0))
        glyph2 = self.getGlyph_generic()
        glyph2.clearAnchors()
        glyph2.appendAnchor("a", (0, 0))
        glyph2.appendAnchor("b", (0, 0))
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertTrue(is_compatible)
        self.assertFalse(report.anchorDifferences)
        self.assertFalse(report.anchorOrderDifference)
        self.assertFalse(report.anchorCountDifference)
        self.assertFalse(report.anchorsMissingFromGlyph1)
        self.assertFalse(report.anchorsMissingFromGlyph2)

    def test_isCompatible_anchors_order(self):
        glyph1 = self.getGlyph_generic()
        glyph1.clearAnchors()
        glyph1.appendAnchor("a", (0, 0))
        glyph1.appendAnchor("b", (0, 0))
        glyph2 = self.getGlyph_generic()
        glyph2.clearAnchors()
        glyph2.appendAnchor("b", (0, 0))
        glyph2.appendAnchor("a", (0, 0))
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertTrue(is_compatible)
        self.assertEqual(report.anchorDifferences, [(0, "a", "b"), (1, "b", "a")])
        self.assertTrue(report.anchorOrderDifference)
        self.assertFalse(report.anchorCountDifference)
        self.assertFalse(report.anchorsMissingFromGlyph1)
        self.assertFalse(report.anchorsMissingFromGlyph2)

    def test_isCompatible_anchors_intersecting(self):
        glyph1 = self.getGlyph_generic()
        glyph1.clearAnchors()
        glyph1.appendAnchor("a", (0, 0))
        glyph1.appendAnchor("b", (0, 0))
        glyph2 = self.getGlyph_generic()
        glyph2.clearAnchors()
        glyph2.appendAnchor("a", (0, 0))
        glyph2.appendAnchor("b", (0, 0))
        glyph2.appendAnchor("b", (0, 0))
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertTrue(is_compatible)
        self.assertEqual(report.anchorDifferences, [(2, None, "b")])
        self.assertFalse(report.anchorOrderDifference)
        self.assertTrue(report.anchorCountDifference)
        self.assertEqual(report.anchorsMissingFromGlyph1, ["b"])
        self.assertFalse(report.anchorsMissingFromGlyph2)

    def test_isCompatible_anchors_disjoint(self):
        glyph1 = self.getGlyph_generic()
        glyph1.clearAnchors()
        glyph1.appendAnchor("x", (0, 0))
        glyph2 = self.getGlyph_generic()
        glyph2.clearAnchors()
        glyph2.appendAnchor("a", (0, 0))
        glyph2.appendAnchor("a", (0, 0))
        glyph2.appendAnchor("b", (0, 0))
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertTrue(is_compatible)
        self.assertEqual(
            report.anchorDifferences, [(0, "x", "a"), (1, None, "a"), (2, None, "b")]
        )
        self.assertFalse(report.anchorOrderDifference)
        self.assertTrue(report.anchorCountDifference)
        self.assertEqual(report.anchorsMissingFromGlyph1, ["a", "a", "b"])
        self.assertEqual(report.anchorsMissingFromGlyph2, ["x"])

    def test_isCompatible_components(self):
        glyph1, _ = self.objectGenerator("glyph")
        glyph1.appendComponent("a")
        glyph1.appendComponent("b")
        glyph2, _ = self.objectGenerator("glyph")
        glyph2.appendComponent("a")
        glyph2.appendComponent("b")
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertTrue(is_compatible)
        self.assertFalse(report.componentDifferences)
        self.assertFalse(report.componentOrderDifference)
        self.assertFalse(report.componentCountDifference)
        self.assertFalse(report.componentsMissingFromGlyph1)
        self.assertFalse(report.componentsMissingFromGlyph2)

    def test_isCompatible_components_order(self):
        glyph1, _ = self.objectGenerator("glyph")
        glyph1.appendComponent("a")
        glyph1.appendComponent("b")
        glyph2, _ = self.objectGenerator("glyph")
        glyph2.appendComponent("b")
        glyph2.appendComponent("a")
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertTrue(is_compatible)
        self.assertEqual(report.componentDifferences, [(0, "a", "b"), (1, "b", "a")])
        self.assertTrue(report.componentOrderDifference)
        self.assertFalse(report.componentCountDifference)
        self.assertFalse(report.componentsMissingFromGlyph1)
        self.assertFalse(report.componentsMissingFromGlyph2)

    def test_isCompatible_components_intersecting(self):
        glyph1, _ = self.objectGenerator("glyph")
        glyph1.appendComponent("a")
        glyph1.appendComponent("b")
        glyph2, _ = self.objectGenerator("glyph")
        glyph2.appendComponent("a")
        glyph2.appendComponent("b")
        glyph2.appendComponent("b")
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertFalse(is_compatible)
        self.assertEqual(report.componentDifferences, [(2, None, "b")])
        self.assertFalse(report.componentOrderDifference)
        self.assertTrue(report.componentCountDifference)
        self.assertEqual(report.componentsMissingFromGlyph1, ["b"])
        self.assertFalse(report.componentsMissingFromGlyph2)

    def test_isCompatible_components_disjoint(self):
        glyph1, _ = self.objectGenerator("glyph")
        glyph1.appendComponent("x")
        glyph2, _ = self.objectGenerator("glyph")
        glyph2.appendComponent("a")
        glyph2.appendComponent("a")
        glyph2.appendComponent("b")
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertFalse(is_compatible)
        self.assertEqual(
            report.componentDifferences, [(0, "x", "a"), (1, None, "a"), (2, None, "b")]
        )
        self.assertFalse(report.componentOrderDifference)
        self.assertTrue(report.componentCountDifference)
        self.assertEqual(report.componentsMissingFromGlyph1, ["a", "a", "b"])
        self.assertEqual(report.componentsMissingFromGlyph2, ["x"])

    def test_isCompatible_components_disjoint_equal_size(self):
        glyph1, _ = self.objectGenerator("glyph")
        glyph1.appendComponent("x")
        glyph1.appendComponent("y")
        glyph2, _ = self.objectGenerator("glyph")
        glyph2.appendComponent("a")
        glyph2.appendComponent("b")
        is_compatible, report = glyph1.isCompatible(glyph2)
        self.assertFalse(is_compatible)
        self.assertEqual(report.componentDifferences, [(0, "x", "a"), (1, "y", "b")])
        self.assertFalse(report.componentOrderDifference)
        self.assertFalse(report.componentCountDifference)
        self.assertEqual(report.componentsMissingFromGlyph1, ["a", "b"])
        self.assertEqual(report.componentsMissingFromGlyph2, ["x", "y"])

    # -------------
    # Interpolation
    # -------------

    def test_interpolate_glyphWidth_without_rounding(self):
        interpolated, _ = self.objectGenerator("glyph")
        glyph_min, _ = self.objectGenerator("glyph")
        glyph_max, _ = self.objectGenerator("glyph")
        glyph_min.width = 1000
        glyph_max.width = 2000
        interpolated.interpolate(0.5154, glyph_min, glyph_max, round=False)
        self.assertEqual(
            interpolated.width,
            1515.4
        )

    def test_interpolate_glyphWidth_with_rounding(self):
        interpolated, _ = self.objectGenerator("glyph")
        glyph_min, _ = self.objectGenerator("glyph")
        glyph_max, _ = self.objectGenerator("glyph")
        glyph_min.width = 1000
        glyph_max.width = 2000
        interpolated.interpolate(0.5154, glyph_min, glyph_max, round=True)
        self.assertEqual(
            interpolated.width,
            1515
        )

    # ---------------
    # Transformations
    # ---------------

    def test_moveBy_only_contours(self):
        glyph = self.getGlyph_generic()
        glyph.moveBy((100, 0))
        self.assertEqual(
            glyph.bounds[0],
            200
        )
        glyph.moveBy((0, 250))
        self.assertEqual(
            glyph.bounds[1],
            240
        )

    # ---
    # API
    # ---

    def test_isEmpty_false_outlines(self):
        glyph = self.getGlyph_generic()
        self.assertFalse(glyph.isEmpty())

    def test_isEmpty_true_clear(self):
        glyph = self.getGlyph_generic()
        glyph.clear()
        self.assertTrue(glyph.isEmpty())

    def test_isEmpty_false_component(self):
        glyph = self.getGlyph_generic()
        glyph.clear()
        glyph.appendComponent("component 1")
        self.assertFalse(glyph.isEmpty())

    def test_removeOverlap(self):
        glyph = self.getGlyph_generic()
        self.assertEquals(len(glyph), 2)
        glyph.removeOverlap()
        self.assertEquals(len(glyph), 1)


def test_generator(test_name, metric, value):
    if '_invalid_' in test_name:
        def test(self):
            glyph = self.getGlyph_generic()
            with self.assertRaises(TypeError):
                setattr(glyph, metric, value)
    else:
        def test(self):
            glyph = self.getGlyph_generic()
            if '_set_' in test_name:
                setattr(glyph, metric, value)
            self.assertEqual(
                getattr(glyph, metric),
                value
            )
    return test


t_names = ('_get', '_set_valid_positive', '_set_valid_negative',
           '_set_valid_zero', '_set_valid_float', '_set_invalid_string',
           '_set_invalid_none')
invalid = ('abc', None)
metrics = {
    'width': (250, 300, -485, 0, 101.5) + invalid,
    'height': (750, 800, -10, 0, 801.5) + invalid,
    'leftMargin': (100, 200, -15, 0, 201.5) + invalid,
    'rightMargin': (50, 80, -20, 0, 81.5) + invalid,
    'bottomMargin': (-10, 150, -35, 0, 151.5) + invalid,
    'topMargin': (650, 750, -250, 0, 751.5) + invalid,
}

for i, t_name_suffix in enumerate(t_names):
    for metric_name, values in metrics.items():
        test_name = 'test_{}{}'.format(metric_name, t_name_suffix)
        test = test_generator(test_name, metric_name, values[i])
        setattr(TestGlyph, test_name, test)
