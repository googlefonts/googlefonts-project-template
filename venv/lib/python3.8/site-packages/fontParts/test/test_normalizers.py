import unittest
from fontParts.base import normalizers


class TestNormalizers(unittest.TestCase):

    # ----
    # Font
    # ----

    def getFont_layers(self):
        font, _ = self.objectGenerator("font")
        for name in ["A", "B", "C", "D", "E"]:
            font.newLayer(name)
        return font

    # normalizeFileFormatVersion

    def test_normalizeFileFormatVersion_int(self):
        result = normalizers.normalizeFileFormatVersion(3)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 3)

    def test_normalizeFileFormatVersion_float(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeFileFormatVersion(3.0)

    def test_normalizeFileFormatVersion_invalid(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeFileFormatVersion("3")

    # normalizeLayerOrder

    def test_normalizeLayerOrder_valid(self):
        font = self.getFont_layers()
        result = normalizers.normalizeLayerOrder(["A", "B", "C", "D", "E"], font)
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, str)
        self.assertEqual(result, (u"A", u"B", u"C", u"D", u"E"))

    def test_normalizeLayerOrder_validTuple(self):
        font = self.getFont_layers()
        result = normalizers.normalizeLayerOrder(tuple(["A", "B", "C", "D", "E"]), font)
        self.assertEqual(result, (u"A", u"B", u"C", u"D", u"E"))

    def test_normalizeLayerOrder_notList(self):
        font = self.getFont_layers()
        with self.assertRaises(TypeError):
            normalizers.normalizeLayerOrder("A B C D E", font)

    def test_normalizeLayerOrder_invalidMember(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphOrder(["A", "B", "C", "D", 2])

    def test_normalizeLayerOrder_notInFont(self):
        font = self.getFont_layers()
        with self.assertRaises(ValueError):
            normalizers.normalizeLayerOrder(["A", "B", "C", "D", "E", "X"], font)

    def test_normalizeLayerOrder_duplicate(self):
        font = self.getFont_layers()
        with self.assertRaises(ValueError):
            normalizers.normalizeLayerOrder(["A", "B", "C", "C", "D", "E"], font)

    # normalizeDefaultLayerName

    def test_normalizeDefaultLayerName_valid(self):
        font = self.getFont_layers()
        result = normalizers.normalizeDefaultLayerName("B", font)
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"B")

    def test_normalizeDefaultLayerName_notValidLayerName(self):
        font = self.getFont_layers()
        with self.assertRaises(TypeError):
            normalizers.normalizeDefaultLayerName(1, font)

    def test_normalizeDefaultLayerName_notInFont(self):
        font = self.getFont_layers()
        with self.assertRaises(ValueError):
            normalizers.normalizeDefaultLayerName("X", font)

    # normalizeGlyphOrder

    def test_normalizeGlyphOrder_valid(self):
        result = normalizers.normalizeGlyphOrder(["A", "B", "C", "D", "E"])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, str)
        self.assertEqual(result, (u"A", u"B", u"C", u"D", u"E"))

    def test_normalizeGlyphOrder_validTuple(self):
        result = normalizers.normalizeGlyphOrder(tuple(["A", "B", "C", "D", "E"]))
        self.assertEqual(result, (u"A", u"B", u"C", u"D", u"E"))

    def test_normalizeGlyphOrder_notList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphOrder("A B C D E")

    def test_normalizeGlyphOrder_invalidMember(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphOrder(["A", "B", "C", "D", 2])

    def test_normalizeGlyphOrder_duplicate(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphOrder(["A", "B", "C", "C", "D", "E"])

    # -------
    # Kerning
    # -------

    # normalizeKerningKey

    def test_normalizeKerningKey_validGlyphs(self):
        result = normalizers.normalizeKerningKey(("A", "B"))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (u"A", u"B"))

    def test_normalizeKerningKey_validGroups(self):
        result = normalizers.normalizeKerningKey(("public.kern1.A", "public.kern2.B"))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (u"public.kern1.A", u"public.kern2.B"))

    def test_normalizeKerningKey_validList(self):
        result = normalizers.normalizeKerningKey(["A", "B"])
        self.assertEqual(result, (u"A", u"B"))

    def test_normalizeKerningKey_notTuple(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeKerningKey("A B")

    def test_normalizeKerningKey_notEnoughMembers(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeKerningKey(("A",))

    def test_normalizeKerningKey_tooManyMembers(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeKerningKey(("A", "B", "C"))

    def test_normalizeKerningKey_memberNotString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeKerningKey(("A", 2))
        with self.assertRaises(TypeError):
            normalizers.normalizeKerningKey((1, "B"))

    def test_normalizeKerningKey_memberNotLongEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeKerningKey(("A", ""))
        with self.assertRaises(ValueError):
            normalizers.normalizeKerningKey(("", "B"))

    def test_normalizeKerningKey_invalidSide1Group(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeKerningKey(("public.kern2.A", "B"))

    def test_normalizeKerningKey_invalidSide2Group(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeKerningKey(("A", "public.kern1.B"))

    # normalizeKerningValue

    def test_normalizeKerningValue_zero(self):
        result = normalizers.normalizeKerningValue(0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_normalizeKerningValue_positiveInt(self):
        result = normalizers.normalizeKerningValue(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeKerningValue_negativeInt(self):
        result = normalizers.normalizeKerningValue(-1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, -1)

    def test_normalizeKerningValue_positiveFloat(self):
        result = normalizers.normalizeKerningValue(1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeKerningValue_negativeFloat(self):
        result = normalizers.normalizeKerningValue(-1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, -1.0)

    def test_normalizeKerningValue_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeKerningValue("1")

    # ------
    # Groups
    # ------

    # normalizeGroupKey

    def test_normalizeGroupKey_valid(self):
        result = normalizers.normalizeGroupKey("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeGroupKey_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGroupKey(1)

    def test_normalizeGroupKey_notLongEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGroupKey("")

    # normalizeGroupValue

    def test_normalizeGroupValue_valid(self):
        result = normalizers.normalizeGroupValue(["A", "B", "C"])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (u"A", u"B", u"C"))

    def test_normalizeGroupValue_validTuple(self):
        result = normalizers.normalizeGroupValue(("A", "B", "C"))
        self.assertEqual(result, (u"A", u"B", u"C"))

    def test_normalizeGroupValue_validEmpty(self):
        result = normalizers.normalizeGroupValue([])
        self.assertEqual(result, tuple())

    def test_normalizeGroupValue_notList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGroupValue("A B C")

    def test_normalizeGroupValue_invalidMember(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGroupValue(["A", "B", 3])

    # --------
    # Features
    # --------

    # normalizeFeatureText

    def test_normalizeFeatureText_valid(self):
        result = normalizers.normalizeFeatureText("test")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"test")

    def test_normalizeFeatureText_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeFeatureText(123)

    # ---
    # Lib
    # ---

    # normalizeLibKey

    def test_normalizeLibKey_valid(self):
        result = normalizers.normalizeLibKey("test")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"test")

    def test_normalizeLibKey_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeLibKey(123)

    def test_normalizeLibKey_emptyString(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeLibKey("")

    # normalizeLibValue

    def test_normalizeLibValue_invalidNone(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeLibValue(None)

    def test_normalizeLibValue_validString(self):
        result = normalizers.normalizeLibValue("test")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"test")

    def test_normalizeLibValue_validInt(self):
        result = normalizers.normalizeLibValue(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeLibValue_validFloat(self):
        result = normalizers.normalizeLibValue(1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeLibValue_validTuple(self):
        result = normalizers.normalizeLibValue(("A", "B"))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (u"A", u"B"))

    def test_normalizeLibValue_invalidTupleMember(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeLibValue((1, None))

    def test_normalizeLibValue_validList(self):
        result = normalizers.normalizeLibValue(["A", "B"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, [u"A", u"B"])

    def test_normalizeLibValue_invalidListMember(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeLibValue([1, None])

    def test_normalizeLibValue_validDict(self):
        result = normalizers.normalizeLibValue({"A": 1, "B": 2})
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {u"A": 1, u"B": 2})

    def test_normalizeLibValue_invalidDictKey(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeLibValue({1: 1, "B": 2})

    def test_normalizeLibValue_invalidDictValue(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeLibValue({"A": None, "B": 2})

    # -----
    # Layer
    # -----

    # normalizeLayer

    def test_normalizeLayer_valid(self):
        from fontParts.base.layer import BaseLayer
        layer, _ = self.objectGenerator("layer")
        result = normalizers.normalizeLayer(layer)
        self.assertIsInstance(result, BaseLayer)
        self.assertEqual(result, layer)

    def test_normalizeLayer_notLayer(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeLayer(123)

    # normalizeLayerName

    def test_normalizeLayerName_valid(self):
        result = normalizers.normalizeLayerName("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeLayerName_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeLayerName(123)

    def test_normalizeLayerName_notLongEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeLayerName("")

    # -----
    # Glyph
    # -----

    # normalizeGlyph

    def test_normalizeGlyph_valid(self):
        from fontParts.base.glyph import BaseGlyph
        glyph, _ = self.objectGenerator("glyph")
        result = normalizers.normalizeGlyph(glyph)
        self.assertIsInstance(result, BaseGlyph)
        self.assertEqual(result, glyph)

    def test_normalizeGlyph_notGlyph(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyph(123)

    # normalizeGlyphName

    def test_normalizeGlyphName_valid(self):
        result = normalizers.normalizeGlyphName("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeGlyphName_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphName(123)

    def test_normalizeGlyphName_notLongEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphName("")

    # normalizeGlyphUnicodes

    def test_normalizeGlyphUnicodes_valid(self):
        result = normalizers.normalizeGlyphUnicodes([1, 2, 3])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1, 2, 3))

    def test_normalizeGlyphUnicodes_validTuple(self):
        result = normalizers.normalizeGlyphUnicodes(tuple([1, 2, 3]))
        self.assertEqual(result, (1, 2, 3))

    def test_normalizeGlyphUnicodes_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphUnicodes("xyz")

    def test_normalizeGlyphUnicodes_invalidDuplicateMembers(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphUnicodes([1, 2, 3, 2])

    def test_normalizeGlyphUnicodes_invalidMember(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphUnicodes([1, 2, "xyz"])

    # normalizeGlyphUnicode

    def test_normalizeGlyphUnicode_validInt(self):
        result = normalizers.normalizeGlyphUnicode(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeGlyphUnicode_validHex(self):
        result = normalizers.normalizeGlyphUnicode("0001")
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeGlyphUnicode_validRangeMinimum(self):
        result = normalizers.normalizeGlyphUnicode(0)
        self.assertEqual(result, 0)

    def test_normalizeGlyphUnicode_validRangeMaximum(self):
        result = normalizers.normalizeGlyphUnicode(1114111)
        self.assertEqual(result, 1114111)

    def test_normalizeGlyphUnicode_invalidFloat(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphUnicode(1.0)

    def test_normalizeGlyphUnicode_invalidString(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphUnicode("xyz")

    def test_normalizeGlyphUnicode_invalidRangeMinimum(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphUnicode(-1)

    def test_normalizeGlyphUnicode_invalidRangeMaximum(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphUnicode(1114112)

    # normalizeGlyphBottomMargin

    def test_normalizeGlyphBottomMargin_zero(self):
        result = normalizers.normalizeGlyphBottomMargin(0)
        self.assertEqual(result, 0)

    def test_normalizeGlyphBottomMargin_positiveInt(self):
        result = normalizers.normalizeGlyphBottomMargin(1)
        self.assertEqual(result, 1)

    def test_normalizeGlyphBottomMargin_negativeInt(self):
        result = normalizers.normalizeGlyphBottomMargin(-1)
        self.assertEqual(result, -1)

    def test_normalizeGlyphBottomMargin_positiveFloat(self):
        result = normalizers.normalizeGlyphBottomMargin(1.01)
        self.assertEqual(result, 1.01)

    def test_normalizeGlyphBottomMargin_negativeFloat(self):
        result = normalizers.normalizeGlyphBottomMargin(-1.01)
        self.assertEqual(result, -1.01)

    def test_normalizeGlyphBottomMargin_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphBottomMargin("1")

    # normalizeGlyphLeftMargin

    def test_normalizeGlyphLeftMargin_zero(self):
        result = normalizers.normalizeGlyphLeftMargin(0)
        self.assertEqual(result, 0)

    def test_normalizeGlyphLeftMargin_positiveInt(self):
        result = normalizers.normalizeGlyphLeftMargin(1)
        self.assertEqual(result, 1)

    def test_normalizeGlyphLeftMargin_negativeInt(self):
        result = normalizers.normalizeGlyphLeftMargin(-1)
        self.assertEqual(result, -1)

    def test_normalizeGlyphLeftMargin_positiveFloat(self):
        result = normalizers.normalizeGlyphLeftMargin(1.01)
        self.assertEqual(result, 1.01)

    def test_normalizeGlyphLeftMargin_negativeFloat(self):
        result = normalizers.normalizeGlyphLeftMargin(-1.01)
        self.assertEqual(result, -1.01)

    def test_normalizeGlyphLeftMargin_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphLeftMargin("1")

    # normalizeGlyphRightMargin

    def test_normalizeGlyphRightMargin_zero(self):
        result = normalizers.normalizeGlyphRightMargin(0)
        self.assertEqual(result, 0)

    def test_normalizeGlyphRightMargin_positiveInt(self):
        result = normalizers.normalizeGlyphRightMargin(1)
        self.assertEqual(result, 1)

    def test_normalizeGlyphRightMargin_negativeInt(self):
        result = normalizers.normalizeGlyphRightMargin(-1)
        self.assertEqual(result, -1)

    def test_normalizeGlyphRightMargin_positiveFloat(self):
        result = normalizers.normalizeGlyphRightMargin(1.01)
        self.assertEqual(result, 1.01)

    def test_normalizeGlyphRightMargin_negativeFloat(self):
        result = normalizers.normalizeGlyphRightMargin(-1.01)
        self.assertEqual(result, -1.01)

    def test_normalizeGlyphRightMargin_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphRightMargin("1")

    # normalizeGlyphHeight

    def test_normalizeGlyphHeight_zero(self):
        result = normalizers.normalizeGlyphHeight(0)
        self.assertEqual(result, 0)

    def test_normalizeGlyphHeight_positiveInt(self):
        result = normalizers.normalizeGlyphHeight(1)
        self.assertEqual(result, 1)

    def test_normalizeGlyphHeight_negativeInt(self):
        result = normalizers.normalizeGlyphHeight(-1)
        self.assertEqual(result, -1)

    def test_normalizeGlyphHeight_positiveFloat(self):
        result = normalizers.normalizeGlyphHeight(1.01)
        self.assertEqual(result, 1.01)

    def test_normalizeGlyphHeight_negativeFloat(self):
        result = normalizers.normalizeGlyphHeight(-1.01)
        self.assertEqual(result, -1.01)

    def test_normalizeGlyphHeight_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphHeight("1")

    # normalizeGlyphTopMargin

    def test_normalizeGlyphTopMargin_zero(self):
        result = normalizers.normalizeGlyphTopMargin(0)
        self.assertEqual(result, 0)

    def test_normalizeGlyphTopMargin_positiveInt(self):
        result = normalizers.normalizeGlyphTopMargin(1)
        self.assertEqual(result, 1)

    def test_normalizeGlyphTopMargin_negativeInt(self):
        result = normalizers.normalizeGlyphTopMargin(-1)
        self.assertEqual(result, -1)

    def test_normalizeGlyphTopMargin_positiveFloat(self):
        result = normalizers.normalizeGlyphTopMargin(1.01)
        self.assertEqual(result, 1.01)

    def test_normalizeGlyphTopMargin_negativeFloat(self):
        result = normalizers.normalizeGlyphTopMargin(-1.01)
        self.assertEqual(result, -1.01)

    def test_normalizeGlyphTopMargin_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphTopMargin("1")

    # normalizeGlyphFormatVersion

    def test_normalizeGlyphFormatVersion_int1(self):
        result = normalizers.normalizeGlyphFormatVersion(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeGlyphFormatVersion_int2(self):
        result = normalizers.normalizeGlyphFormatVersion(2)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 2)

    def test_normalizeGlyphFormatVersion_int3(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphFormatVersion(3)

    def test_normalizeGlyphFormatVersion_float1(self):
        result = normalizers.normalizeGlyphFormatVersion(1.0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeGlyphFormatVersion_float2(self):
        result = normalizers.normalizeGlyphFormatVersion(2.0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 2)

    def test_normalizeGlyphFormatVersion_float3(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGlyphFormatVersion(3.0)

    def test_normalizeGlyphFormatVersion_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphFormatVersion("1")

    # -------
    # Contour
    # -------

    # normalizeContour

    def test_normalizeContour_valid(self):
        from fontParts.base.contour import BaseContour
        contour, _ = self.objectGenerator("contour")
        result = normalizers.normalizeContour(contour)
        self.assertIsInstance(result, BaseContour)
        self.assertEqual(result, contour)

    def test_normalizeContour_notContour(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeContour(123)

    # -----
    # Point
    # -----

    # normalizePoint

    def test_normalizePoint_valid(self):
        from fontParts.base.point import BasePoint
        point, _ = self.objectGenerator("point")
        result = normalizers.normalizePoint(point)
        self.assertIsInstance(result, BasePoint)
        self.assertEqual(result, point)

    def test_normalizePoint_notPoint(self):
        with self.assertRaises(TypeError):
            normalizers.normalizePoint(123)

    # normalizePointType

    def test_normalizePointType_move(self):
        result = normalizers.normalizePointType("move")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"move")

    def test_normalizePointType_Move(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("Move")

    def test_normalizePointType_MOVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("MOVE")

    def test_normalizePointType_line(self):
        result = normalizers.normalizePointType("line")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"line")

    def test_normalizePointType_Line(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("Line")

    def test_normalizePointType_LINE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("LINE")

    def test_normalizePointType_offcurve(self):
        result = normalizers.normalizePointType("offcurve")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"offcurve")

    def test_normalizePointType_OffCurve(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("OffCurve")

    def test_normalizePointType_OFFCURVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("OFFCURVE")

    def test_normalizePointType_curve(self):
        result = normalizers.normalizePointType("curve")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"curve")

    def test_normalizePointType_Curve(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("Curve")

    def test_normalizePointType_CURVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("CURVE")

    def test_normalizePointType_qcurve(self):
        result = normalizers.normalizePointType("qcurve")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"qcurve")

    def test_normalizePointType_QOffCurve(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("QCurve")

    def test_normalizePointType_QOFFCURVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("QCURVE")

    def test_normalizePointType_unknown(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointType("unknonwn")

    def test_normalizePointType_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizePointType(123)

    # normalizePointName

    def test_normalizePointName_valid(self):
        result = normalizers.normalizePointName("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizePointName_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizePointName(123)

    def test_normalizePointName_notLongEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizePointName("")

    # -------
    # Segment
    # -------

    # normalizeSegment

    def test_normalizeSegment_valid(self):
        from fontParts.base.segment import BaseSegment
        segment, _ = self.objectGenerator("segment")
        result = normalizers.normalizeSegment(segment)
        self.assertIsInstance(result, BaseSegment)
        self.assertEqual(result, segment)

    def test_normalizePoint_notContour(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeSegment(123)

    # normalizeSegmentType

    def test_normalizeSegmentType_move(self):
        result = normalizers.normalizeSegmentType("move")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"move")

    def test_normalizeSegmentType_Move(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("Move")

    def test_normalizeSegmentType_MOVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("MOVE")

    def test_normalizeSegmentType_line(self):
        result = normalizers.normalizeSegmentType("line")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"line")

    def test_normalizeSegmentType_Line(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("Line")

    def test_normalizeSegmentType_LINE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("LINE")

    def test_normalizeSegmentType_curve(self):
        result = normalizers.normalizeSegmentType("curve")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"curve")

    def test_normalizeSegmentType_OffCurve(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("Curve")

    def test_normalizeSegmentType_OFFCURVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("CURVE")

    def test_normalizeSegmentType_qcurve(self):
        result = normalizers.normalizeSegmentType("qcurve")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"qcurve")

    def test_normalizeSegmentType_QOffCurve(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("QCurve")

    def test_normalizeSegmentType_QOFFCURVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("QCURVE")

    def test_normalizeSegmentType_unknown(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeSegmentType("offcurve")

    def test_normalizeSegmentType_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeSegmentType(123)

    # ------
    # BPoint
    # ------

    # normalizeBPoint

    def test_normalizeBPoint_valid(self):
        from fontParts.base.bPoint import BaseBPoint
        bPoint, _ = self.objectGenerator("bPoint")
        result = normalizers.normalizeBPoint(bPoint)
        self.assertIsInstance(result, BaseBPoint)
        self.assertEqual(result, bPoint)

    def test_normalizeBPoint_notBPoint(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeBPoint(123)

    # normalizeBPointType

    def test_normalizeBPointType_corner(self):
        result = normalizers.normalizeBPointType("corner")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"corner")

    def test_normalizeBPointType_Corner(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBPointType("Corner")

    def test_normalizeBPointType_CORNER(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBPointType("CORNER")

    def test_normalizeBPointType_curve(self):
        result = normalizers.normalizeBPointType("curve")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"curve")

    def test_normalizeBPointType_OffCurve(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBPointType("Curve")

    def test_normalizeBPointType_OFFCURVE(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBPointType("CURVE")

    def test_normalizeBPointType_unknown(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBPointType("offcurve")

    def test_normalizeBPointType_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeBPointType(123)

    # ---------
    # Component
    # ---------

    # normalizeComponent

    def test_normalizeComponent_valid(self):
        from fontParts.base.component import BaseComponent
        component, _ = self.objectGenerator("component")
        result = normalizers.normalizeComponent(component)
        self.assertIsInstance(result, BaseComponent)
        self.assertEqual(result, component)

    def test_normalizeComponent_notComponent(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeComponent(123)

    # normalizeComponentScale

    def test_normalizeComponentScale_tupleZero(self):
        result = normalizers.normalizeComponentScale((0, 0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (0, 0))

    def test_normalizeComponentScale_tuplePositiveInt(self):
        result = normalizers.normalizeComponentScale((2, 2))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeComponentScale_tupleNegativeInt(self):
        result = normalizers.normalizeComponentScale((-2, -2))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeComponentScale_tuplePositiveFloat(self):
        result = normalizers.normalizeComponentScale((2.0, 2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeComponentScale_tupleNegativeFloat(self):
        result = normalizers.normalizeComponentScale((-2.0, -2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeComponentScale_listZero(self):
        result = normalizers.normalizeComponentScale([0, 0])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (0, 0))

    def test_normalizeComponentScale_listPositiveInt(self):
        result = normalizers.normalizeComponentScale([2, 2])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeComponentScale_listNegativeInt(self):
        result = normalizers.normalizeComponentScale([-2, -2])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeComponentScale_listPositiveFloat(self):
        result = normalizers.normalizeComponentScale([2.0, 2.0])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeComponentScale_listNegativeFloat(self):
        result = normalizers.normalizeComponentScale([-2.0, -2.0])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeComponentScale_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeComponentScale("2, 2")

    def test_normalizeComponentScale_numberNotNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeComponentScale((2, "2"))

    def test_normalizeComponentScale_notNumberNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeComponentScale(("2", 2))

    def test_normalizeComponentScale_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeComponentScale((2,))

    def test_normalizeComponentScale_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeComponentScale((2, 2, 2))

    # ------
    # Anchor
    # ------

    # normalizeAnchor

    def test_normalizeAnchor_valid(self):
        from fontParts.base.anchor import BaseAnchor
        anchor, _ = self.objectGenerator("anchor")
        result = normalizers.normalizeAnchor(anchor)
        self.assertIsInstance(result, BaseAnchor)
        self.assertEqual(result, anchor)

    def test_normalizeAnchor_notAnchor(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeAnchor(123)

    # normalizeAnchorName

    def test_normalizeAnchorName_valid(self):
        result = normalizers.normalizeAnchorName("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeAnchorName_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeAnchorName(123)

    def test_normalizeAnchorName_notLongEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeAnchorName("")

    # ---------
    # Guideline
    # ---------

    # normalizeGuideline

    def test_normalizeGuideline_valid(self):
        from fontParts.base.guideline import BaseGuideline
        guideline, _ = self.objectGenerator("guideline")
        result = normalizers.normalizeGuideline(guideline)
        self.assertIsInstance(result, BaseGuideline)
        self.assertEqual(result, guideline)

    def test_normalizeGuideline_notGuideline(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGuideline(123)

    # normalizeGuidelineName

    def test_normalizeGuidelineName_valid(self):
        result = normalizers.normalizeGuidelineName("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeGuidelineName_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGuidelineName(123)

    def test_normalizeGuidelineName_notLongEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeGuidelineName("")

    # -------
    # Generic
    # -------

    # normalizeBoolean

    def test_normalizeBoolean_true(self):
        result = normalizers.normalizeBoolean(True)
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)

    def test_normalizeBoolean_false(self):
        result = normalizers.normalizeBoolean(False)
        self.assertIsInstance(result, bool)
        self.assertEqual(result, False)

    def test_normalizeBoolean_1(self):
        result = normalizers.normalizeBoolean(1)
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)

    def test_normalizeBoolean_0(self):
        result = normalizers.normalizeBoolean(0)
        self.assertIsInstance(result, bool)
        self.assertEqual(result, False)

    def test_normalizeBoolean_10(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBoolean(10)

    def test_normalizeBoolean_string(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBoolean("True")

    # normalizeIndex

    def test_normalizeIndex_zero(self):
        result = normalizers.normalizeIndex(0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_normalizeIndex_positiveInt(self):
        result = normalizers.normalizeIndex(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeIndex_negativeInt(self):
        result = normalizers.normalizeIndex(-1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, -1)

    def test_normalizeIndex_notInt(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeIndex(1.0)

    # normalizeIdentifier

    def test_normalizeIdentifier_none(self):
        result = normalizers.normalizeIdentifier(None)
        self.assertEqual(result, None)

    def test_normalizeIdentifier_stringMinimumLength(self):
        result = normalizers.normalizeIdentifier("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeIdentifier_stringMaximumLength(self):
        result = normalizers.normalizeIdentifier("A" * 100)
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A" * 100)

    def test_normalizeIdentifier_stringMinimumCharacter(self):
        result = normalizers.normalizeIdentifier(chr(0x20))
        self.assertIsInstance(result, str)
        self.assertEqual(result, chr(0x20))

    def test_normalizeIdentifier_stringMaximumCharacter(self):
        result = normalizers.normalizeIdentifier(chr(0x7E))
        self.assertIsInstance(result, str)
        self.assertEqual(result, chr(0x7E))

    def test_normalizeIdentifier_stringTooShort(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeIdentifier("")

    def test_normalizeIdentifier_stringTooLong(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeIdentifier("A" * 101)

    def test_normalizeIdentifier_stringBeforeMinimumCharacter(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeIdentifier(chr(0x20 - 1))

    def test_normalizeIdentifier_stringAfterMaximumCharacter(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeIdentifier(chr(0x7E + 1))

    def test_normalizeIdentifier_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeIdentifier(1)

    # normalizeX

    def test_normalizeX_zero(self):
        result = normalizers.normalizeX(0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_normalizeX_positiveInt(self):
        result = normalizers.normalizeX(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeX_negativeInt(self):
        result = normalizers.normalizeX(-1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, -1)

    def test_normalizeX_positiveFloat(self):
        result = normalizers.normalizeX(1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeX_negativeFloat(self):
        result = normalizers.normalizeX(-1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, -1.0)

    def test_normalizeX_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeX("1")

    # normalizeY

    def test_normalizeY_zero(self):
        result = normalizers.normalizeY(0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_normalizeY_positiveInt(self):
        result = normalizers.normalizeY(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeY_negativeInt(self):
        result = normalizers.normalizeY(-1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, -1)

    def test_normalizeY_positiveFloat(self):
        result = normalizers.normalizeY(1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeY_negativeFloat(self):
        result = normalizers.normalizeY(-1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, -1.0)

    def test_normalizeY_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeY("1")

    # normalizeCoordinateTuple

    def test_normalizeCoordinateTuple_list(self):
        result = normalizers.normalizeCoordinateTuple([1, 1])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1, 1))

    def test_normalizeCoordinateTuple_zero(self):
        result = normalizers.normalizeCoordinateTuple((0, 0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0))

    def test_normalizeCoordinateTuple_positiveInt(self):
        result = normalizers.normalizeCoordinateTuple((1, 1))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1, 1))

    def test_normalizeCoordinateTuple_negativeInt(self):
        result = normalizers.normalizeCoordinateTuple((-1, -1))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-1, -1))

    def test_normalizeCoordinateTuple_positiveFloat(self):
        result = normalizers.normalizeCoordinateTuple((1.0, 1.0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 1.0))

    def test_normalizeCoordinateTuple_negativeFloat(self):
        result = normalizers.normalizeCoordinateTuple((-1.0, -1.0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-1.0, -1.0))

    def test_normalizeCoordinateTuple_numberNotNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeCoordinateTuple((1, "1"))

    def test_normalizeCoordinateTuple_notNumberNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeCoordinateTuple(("1", 1))

    def test_normalizeCoordinateTuple_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeCoordinateTuple((1,))

    def test_normalizeCoordinateTuple_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeCoordinateTuple((1, 1, 1))

    # normalizeBoundingBox

    def test_normalizeBoundingBox_tuple(self):
        result = normalizers.normalizeBoundingBox((1, 2, 3, 4))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0))

    def test_normalizeBoundingBox_list(self):
        result = normalizers.normalizeBoundingBox([1, 2, 3, 4])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0))

    def test_normalizeBoundingBox_int(self):
        result = normalizers.normalizeBoundingBox((1, 2, 3, 4))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0))

    def test_normalizeBoundingBox_float(self):
        result = normalizers.normalizeBoundingBox((1.0, 2.0, 3.0, 4.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0))

    def test_normalizeBoundingBox_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBoundingBox((1, 2, 3))

    def test_normalizeBoundingBox_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBoundingBox((1, 2, 3, 4, 5))

    def test_normalizeBoundingBox_notListOrTuple(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeBoundingBox("1 2 3 4")

    def test_normalizeBoundingBox_invalidMember(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeBoundingBox((1, 2, "3", 4))

    def test_normalizeBoundingBox_xMinSameAsXMax(self):
        result = normalizers.normalizeBoundingBox((1, 2, 1, 4))
        self.assertEqual(result, (1.0, 2.0, 1.0, 4.0))

    def test_normalizeBoundingBox_yMinSameAsYMax(self):
        result = normalizers.normalizeBoundingBox((1, 2, 3, 2))
        self.assertEqual(result, (1.0, 2.0, 3.0, 2.0))

    def test_normalizeBoundingBox_xMaxLessThanXMin(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBoundingBox((1, 2, 0, 4))

    def test_normalizeBoundingBox_yMaxLessThanYMin(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeBoundingBox((1, 2, 3, 1))

    # normalizeArea

    def test_normalizeArea_zero(self):
        result = normalizers.normalizeArea(0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0)

    def test_normalizeArea_positiveInt(self):
        result = normalizers.normalizeArea(1)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeArea_positiveFloat(self):
        result = normalizers.normalizeArea(1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeArea_negativeInt(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeArea(-1)

    def test_normalizeArea_negativeFloat(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeArea(-1.0)

    def test_normalizeArea_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeArea("1")

    # normalizeColor

    def test_normalizeColor_color(self):
        from fontParts.base.color import Color
        result = normalizers.normalizeColor(Color((0, 0, 0, 0)))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0, 0, 0))

    def test_normalizeColor_tuple(self):
        result = normalizers.normalizeColor((0, 0, 0, 0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0, 0, 0))

    def test_normalizeColor_list(self):
        result = normalizers.normalizeColor([0, 0, 0, 0])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0, 0, 0))

    def test_normalizeColor_ints(self):
        result = normalizers.normalizeColor((1, 1, 1, 1))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 1.0, 1.0, 1.0))

    def test_normalizeColor_floats(self):
        result = normalizers.normalizeColor((1.0, 1.0, 1.0, 1.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 1.0, 1.0, 1.0))

    def test_normalizeColor_tooSmall(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((-1, 1, 1, 1))
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, -1, 1, 1))
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, 1, -1, 1))
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, 1, 1, -1))

    def test_normalizeColor_tooLarge(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((2, 1, 1, 1))
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, 2, 1, 1))
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, 1, 2, 1))
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, 1, 1, 2))

    def test_normalizeColor_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, 1, 1))

    def test_normalizeColor_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeColor((1, 1, 1, 1, 1))

    def test_normalizeColor_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeColor("1,1,1,1")

    def test_normalizeColor_invalidMember(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeColor((1, "1", 1, 1))

    # normalizeGlyphNote

    def test_normalizeGlyphNote_string(self):
        result = normalizers.normalizeGlyphNote("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeGlyphNote_emptyString(self):
        result = normalizers.normalizeGlyphNote("")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"")

    def test_normalizeGlyphNote_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeGlyphNote(123)

    # normalizeFilePath

    def test_normalizeFilePath_string(self):
        result = normalizers.normalizeFilePath("A")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"A")

    def test_normalizeFilePath_emptyString(self):
        result = normalizers.normalizeFilePath("")
        self.assertIsInstance(result, str)
        self.assertEqual(result, u"")

    def test_normalizeFilePath_notString(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeFilePath(123)

    # normalizeInterpolationFactor

    def test_normalizeInterpolationFactor_zero(self):
        result = normalizers.normalizeInterpolationFactor(0)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0))

    def test_normalizeInterpolationFactor_positiveInt(self):
        result = normalizers.normalizeInterpolationFactor(1)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 1.0))

    def test_normalizeInterpolationFactor_negativeInt(self):
        result = normalizers.normalizeInterpolationFactor(-1)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-1.0, -1.0))

    def test_normalizeInterpolationFactor_positiveFloat(self):
        result = normalizers.normalizeInterpolationFactor(1.0)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 1.0))

    def test_normalizeInterpolationFactor_negativeFloat(self):
        result = normalizers.normalizeInterpolationFactor(-1.0)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-1.0, -1.0))

    def test_normalizeInterpolationFactor_tupleZero(self):
        result = normalizers.normalizeInterpolationFactor((0, 0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (0, 0))

    def test_normalizeInterpolationFactor_tuplePositiveInt(self):
        result = normalizers.normalizeInterpolationFactor((2, 2))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeInterpolationFactor_tupleNegativeInt(self):
        result = normalizers.normalizeInterpolationFactor((-2, -2))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeInterpolationFactor_tuplePositiveFloat(self):
        result = normalizers.normalizeInterpolationFactor((2.0, 2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeInterpolationFactor_tupleNegativeFloat(self):
        result = normalizers.normalizeInterpolationFactor((-2.0, -2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeInterpolationFactor_listZero(self):
        result = normalizers.normalizeInterpolationFactor([0, 0])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (0, 0))

    def test_normalizeInterpolationFactor_listPositiveInt(self):
        result = normalizers.normalizeInterpolationFactor([2, 2])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeInterpolationFactor_listNegativeInt(self):
        result = normalizers.normalizeInterpolationFactor([-2, -2])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeInterpolationFactor_listPositiveFloat(self):
        result = normalizers.normalizeInterpolationFactor([2.0, 2.0])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeInterpolationFactor_listNegativeFloat(self):
        result = normalizers.normalizeInterpolationFactor([-2.0, -2.0])
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeInterpolationFactor_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeInterpolationFactor("2, 2")

    def test_normalizeInterpolationFactor_numberNotNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeInterpolationFactor((2, "2"))

    def test_normalizeInterpolationFactor_notNumberNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeInterpolationFactor(("2", 2))

    def test_normalizeInterpolationFactor_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeInterpolationFactor((2,))

    def test_normalizeInterpolationFactor_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeInterpolationFactor((2, 2, 2))

    # normalizeRotationAngle

    def test_normalizeRotationAngle_zero(self):
        result = normalizers.normalizeRotationAngle(0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0)

    def test_normalizeRotationAngle_positiveInt(self):
        result = normalizers.normalizeRotationAngle(1)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeRotationAngle_negativeInt(self):
        result = normalizers.normalizeRotationAngle(-1)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 359.0)

    def test_normalizeRotationAngle_positiveFloat(self):
        result = normalizers.normalizeRotationAngle(1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_normalizeRotationAngle_negativeFloat(self):
        result = normalizers.normalizeRotationAngle(-1.0)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 359.0)

    def test_normalizeRotationAngle_maximum(self):
        result = normalizers.normalizeRotationAngle(360)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 360.0)

    def test_normalizeRotationAngle_minimum(self):
        result = normalizers.normalizeRotationAngle(-360)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0)

    def test_normalizeRotationAngle_moreThanMaximum(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeRotationAngle(361)

    def test_normalizeRotationAngle_lessThanMaximum(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeRotationAngle(-361)

    def test_normalizeRotationAngle_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeRotationAngle("1")

    # ---------------
    # Transformations
    # ---------------

    # normalizeTransformationMatrix

    def test_normalizeTransformationMatrix_tuple(self):
        result = normalizers.normalizeTransformationMatrix((1, 2, 3, 4, 5, 6))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0, 5.0, 6.0))

    def test_normalizeTransformationMatrix_list(self):
        result = normalizers.normalizeTransformationMatrix([1, 2, 3, 4, 5, 6])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0, 5.0, 6.0))

    def test_normalizeTransformationMatrix_positiveInts(self):
        result = normalizers.normalizeTransformationMatrix((1, 2, 3, 4, 5, 6))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0, 5.0, 6.0))

    def test_normalizeTransformationMatrix_positiveFloats(self):
        result = normalizers.normalizeTransformationMatrix((1.0, 2.0, 3.0, 4.0, 5.0, 6.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 2.0, 3.0, 4.0, 5.0, 6.0))

    def test_normalizeTransformationMatrix_negativeInts(self):
        result = normalizers.normalizeTransformationMatrix((-1, -2, -3, -4, -5, -6))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-1.0, -2.0, -3.0, -4.0, -5.0, -6.0))

    def test_normalizeTransformationMatrix_negativeFloats(self):
        result = normalizers.normalizeTransformationMatrix((-1.0, -2.0, -3.0,
                                                            -4.0, -5.0, -6.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-1.0, -2.0, -3.0, -4.0, -5.0, -6.0))

    def test_normalizeTransformationMatrix_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationMatrix((1, 2, 3, 4, 5))

    def test_normalizeTransformationMatrix_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationMatrix((1, 2, 3, 4, 5, 6, 7))

    def test_normalizeTransformationMatrix_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationMatrix("1 2 3 4 5 6")

    def test_normalizeTransformationMatrix_invalidMember(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationMatrix((1, 2, 3, "4", 5, 6))

    # normalizeTransformationOffset

    def test_normalizeTransformationOffset_tupleZero(self):
        result = normalizers.normalizeTransformationOffset((0, 0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0))

    def test_normalizeTransformationOffset_tuplePositiveInt(self):
        result = normalizers.normalizeTransformationOffset((2, 2))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationOffset_tupleNegativeInt(self):
        result = normalizers.normalizeTransformationOffset((-2, -2))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationOffset_tuplePositiveFloat(self):
        result = normalizers.normalizeTransformationOffset((2.0, 2.0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationOffset_tupleNegativeFloat(self):
        result = normalizers.normalizeTransformationOffset((-2.0, -2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationOffset_listZero(self):
        result = normalizers.normalizeTransformationOffset([0, 0])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0))

    def test_normalizeTransformationOffset_listPositiveInt(self):
        result = normalizers.normalizeTransformationOffset([2, 2])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationOffset_listNegativeInt(self):
        result = normalizers.normalizeTransformationOffset([-2, -2])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationOffset_listPositiveFloat(self):
        result = normalizers.normalizeTransformationOffset([2.0, 2.0])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationOffset_listNegativeFloat(self):
        result = normalizers.normalizeTransformationOffset([-2.0, -2.0])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationOffset_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationOffset("2, 2")

    def test_normalizeTransformationOffset_numberNotNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationOffset((2, "2"))

    def test_normalizeTransformationOffset_notNumberNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationOffset(("2", 2))

    def test_normalizeTransformationOffset_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationOffset((2,))

    def test_normalizeTransformationOffset_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationOffset((2, 2, 2))

    # normalizeTransformationSkewAngle

    def test_normalizeTransformationSkewAngle_int(self):
        result = normalizers.normalizeTransformationSkewAngle(1)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 0))

    def test_normalizeTransformationSkewAngle_float(self):
        result = normalizers.normalizeTransformationSkewAngle(1.0)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 0))

    def test_normalizeTransformationSkewAngle_list(self):
        result = normalizers.normalizeTransformationSkewAngle([1, 2])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0))

    def test_normalizeTransformationSkewAngle_tuple(self):
        result = normalizers.normalizeTransformationSkewAngle((1, 2))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0))

    def test_normalizeTransformationSkewAngle_zero(self):
        result = normalizers.normalizeTransformationSkewAngle((0, 0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (0, 0))

    def test_normalizeTransformationSkewAngle_positiveInts(self):
        result = normalizers.normalizeTransformationSkewAngle((1, 2))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 2.0))

    def test_normalizeTransformationSkewAngle_negativeInts(self):
        result = normalizers.normalizeTransformationSkewAngle((-1, -2))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (359.0, 358.0))

    def test_normalizeTransformationSkewAngle_positiveFloats(self):
        result = normalizers.normalizeTransformationSkewAngle((1.0, 2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (1.0, 2.0))

    def test_normalizeTransformationSkewAngle_negativeFloats(self):
        result = normalizers.normalizeTransformationSkewAngle((-1.0, -2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (359.0, 358.0))

    def test_normalizeTransformationSkewAngle_tooLow(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationSkewAngle((-361, -361))

    def test_normalizeTransformationSkewAngle_tooHigh(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationSkewAngle((361, 361))

    def test_normalizeTransformationSkewAngle_numberNotNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationSkewAngle((1, "2"))

    def test_normalizeTransformationSkewAngle_notNumberNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationSkewAngle(("1", 1))

    def test_normalizeTransformationSkewAngle_tooFew(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationSkewAngle(tuple())

    def test_normalizeTransformationSkewAngle_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationSkewAngle((1, 2, 3))

    def test_normalizeTransformationSkewAngle_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationSkewAngle("1")

    # normalizeTransformationScale

    def test_normalizeTransformationScale_int(self):
        result = normalizers.normalizeTransformationScale(1)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 1.0))

    def test_normalizeTransformationScale_float(self):
        result = normalizers.normalizeTransformationScale(1.0)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 1.0))

    def test_normalizeTransformationScale_list(self):
        result = normalizers.normalizeTransformationScale([1, 2])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0))

    def test_normalizeTransformationScale_tuple(self):
        result = normalizers.normalizeTransformationScale((1, 2))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (1.0, 2.0))

    def test_normalizeTransformationScale_tupleZero(self):
        result = normalizers.normalizeTransformationScale((0, 0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0))

    def test_normalizeTransformationScale_tuplePositiveInt(self):
        result = normalizers.normalizeTransformationScale((2, 2))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationScale_tupleNegativeInt(self):
        result = normalizers.normalizeTransformationScale((-2, -2))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationScale_tuplePositiveFloat(self):
        result = normalizers.normalizeTransformationScale((2.0, 2.0))
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationScale_tupleNegativeFloat(self):
        result = normalizers.normalizeTransformationScale((-2.0, -2.0))
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, float)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationScale_listZero(self):
        result = normalizers.normalizeTransformationScale([0, 0])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (0, 0))

    def test_normalizeTransformationScale_listPositiveInt(self):
        result = normalizers.normalizeTransformationScale([2, 2])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationScale_listNegativeInt(self):
        result = normalizers.normalizeTransformationScale([-2, -2])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationScale_listPositiveFloat(self):
        result = normalizers.normalizeTransformationScale([2.0, 2.0])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (2.0, 2.0))

    def test_normalizeTransformationScale_listNegativeFloat(self):
        result = normalizers.normalizeTransformationScale([-2.0, -2.0])
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (-2.0, -2.0))

    def test_normalizeTransformationScale_notTupleOrList(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationScale("2, 2")

    def test_normalizeTransformationScale_numberNotNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationScale((2, "2"))

    def test_normalizeTransformationScale_notNumberNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeTransformationScale(("2", 2))

    def test_normalizeTransformationScale_notEnough(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationScale((2,))

    def test_normalizeTransformationScale_tooMany(self):
        with self.assertRaises(ValueError):
            normalizers.normalizeTransformationScale((2, 2, 2))

    # normalizeVisualRounding

    def test_normalizeVisualRounding_int(self):
        result = normalizers.normalizeVisualRounding(1)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeVisualRounding_float(self):
        result = normalizers.normalizeVisualRounding(1.0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_normalizeVisualRounding_half(self):
        result = normalizers.normalizeVisualRounding(1.5)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 2)

    def test_normalizeVisualRounding_half_even(self):
        result = normalizers.normalizeVisualRounding(2.5)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 3)

    def test_normalizeVisualRounding_notNumber(self):
        with self.assertRaises(TypeError):
            normalizers.normalizeVisualRounding("1")
