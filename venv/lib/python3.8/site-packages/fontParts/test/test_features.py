import unittest
import collections


class TestFeatures(unittest.TestCase):

    def getFeatures_generic(self):
        features, _ = self.objectGenerator("features")
        features.text = "# test"
        return features

    # ----
    # repr
    # ----

    def test_reprContents(self):
        font, _ = self.objectGenerator("font")
        features = font.features
        features.text = "# test"
        value = features._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noFont(self):
        features, _ = self.objectGenerator("features")
        features.text = "# test"
        value = features._reprContents()
        self.assertIsInstance(value, list)
        self.assertListEqual(value, [])

    # ----
    # Text
    # ----

    def test_text_get(self):
        features = self.getFeatures_generic()
        self.assertEqual(
            features.text,
            "# test"
        )

    def test_text_valid_set(self):
        features = self.getFeatures_generic()
        features.text = "# foo"
        self.assertEqual(
            features.text,
            "# foo"
        )

    def test_text_set_none(self):
        features = self.getFeatures_generic()
        features.text = None
        self.assertIsNone(features.text)

    def test_text_invalid_set(self):
        features = self.getFeatures_generic()
        with self.assertRaises(TypeError):
            features.text = 123

    # -------
    # Parents
    # -------

    def test_get_parent_font(self):
        font, _ = self.objectGenerator("font")
        features = font.features
        features.text = "# Test"
        self.assertIsNotNone(features.font)
        self.assertEqual(
            features.font,
            font
        )

    def test_get_parent_noFont(self):
        features = self.getFeatures_generic()
        self.assertIsNone(features.font)

    def test_set_parent_font(self):
        font, _ = self.objectGenerator("font")
        features = self.getFeatures_generic()
        features.font = font
        self.assertIsNotNone(features.font)
        self.assertEqual(
            features.font,
            font
        )

    def test_set_parent_font_none(self):
        features = self.getFeatures_generic()
        features.font = None
        self.assertIsNone(features.font)

    def test_set_parent_font_exists(self):
        font, _ = self.objectGenerator("font")
        otherFont, _ = self.objectGenerator("font")
        features = font.features
        features.text = "# Test"
        with self.assertRaises(AssertionError):
            features.font = otherFont

    # ----
    # Hash
    # ----

    def test_hash(self):
        features = self.getFeatures_generic()
        self.assertEqual(
            isinstance(features, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        features_one = self.getFeatures_generic()
        self.assertEqual(
            features_one,
            features_one
        )

    def test_object_not_equal_other(self):
        features_one = self.getFeatures_generic()
        features_two = self.getFeatures_generic()
        self.assertNotEqual(
            features_one,
            features_two
        )

    def test_object_equal_self_variable_assignment(self):
        features_one = self.getFeatures_generic()
        a = features_one
        a.text += "# testing"
        self.assertEqual(
            features_one,
            a
        )

    def test_object_not_equal_self_variable_assignment(self):
        features_one = self.getFeatures_generic()
        features_two = self.getFeatures_generic()
        a = features_one
        self.assertNotEqual(
            features_two,
            a
        )
