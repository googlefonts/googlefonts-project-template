import unittest
import collections


class TestGroups(unittest.TestCase):

    def getGroups_generic(self):
        groups, _ = self.objectGenerator("groups")
        groups.update({
            "group 1": ["A", "B", "C"],
            "group 2": ["x", "y", "z"],
            "group 3": [],
            "group 4": ["A"]
        })
        return groups

    # ----
    # repr
    # ----

    def test_reprContents(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        value = groups._reprContents()
        self.assertIsInstance(value, list)
        found = False
        for i in value:
            self.assertIsInstance(i, str)
            if "for font" in value:
                found = True
        self.assertTrue(found)

    def test_reprContents_noFont(self):
        groups, _ = self.objectGenerator("groups")
        value = groups._reprContents()
        self.assertIsInstance(value, list)
        self.assertEqual(value, [])


    # -------
    # Parents
    # -------

    def test_get_parent_font(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        self.assertIsNotNone(groups.font)
        self.assertEqual(
            groups.font,
            font
        )

    def test_get_parent_font_none(self):
        groups, _ = self.objectGenerator("groups")
        self.assertIsNone(groups.font)

    def test_set_parent_font(self):
        font, _ = self.objectGenerator("font")
        groups, _ = self.objectGenerator("groups")
        groups.font = font
        self.assertIsNotNone(groups.font)
        self.assertEqual(
            groups.font,
            font
        )

    def test_set_parent_font_none(self):
        groups, _ = self.objectGenerator("groups")
        groups.font = None
        self.assertIsNone(groups.font)

    def test_set_parent_differentFont(self):
        font, _ = self.objectGenerator("font")
        fontB, _ = self.objectGenerator("font")
        groups, _ = self.objectGenerator("groups")
        groups.font = font
        self.assertIsNotNone(groups.font)

        with self.assertRaises(AssertionError):
            groups.font = fontB

    # ---
    # len
    # ---

    def test_len_initial(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            len(groups),
            4
        )

    def test_len_clear(self):
        groups = self.getGroups_generic()
        groups.clear()
        self.assertEqual(
            len(groups),
            0
        )

    def test_len_add(self):
        groups = self.getGroups_generic()
        groups['group 5'] = ["D","E","F"]
        self.assertEqual(
            len(groups),
            5
        )

    def test_len_subtract(self):
        groups = self.getGroups_generic()
        groups.pop('group 4')
        self.assertEqual(
            len(groups),
            3
        )



    # ---
    # Get
    # ---

    def test_get_fallback_default(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            groups.get("test"),
            None
        )

    # -------
    # Queries
    # -------

    def test_find_found(self):
        groups = self.getGroups_generic()
        found = groups.findGlyph("A")
        found.sort()
        self.assertEqual(
            found,
            [u"group 1", u"group 4"]
        )

    def test_find_not_found(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            groups.findGlyph("five"),
            []
        )

    def test_find_invalid_key(self):
        groups = self.getGroups_generic()
        with self.assertRaises(TypeError):
            groups.findGlyph(5)

    def test_contains_found(self):
        groups = self.getGroups_generic()
        self.assertTrue("group 4" in groups)

    def test_contains_not_found(self):
        groups = self.getGroups_generic()
        self.assertFalse("group five" in groups)

    def test_get_found(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            groups["group 1"],
            ("A", "B", "C")
        )

    def test_get_not_found(self):
        groups = self.getGroups_generic()
        with self.assertRaises(KeyError):
            groups["group two"]

    # --------------
    # Kerning Groups
    # --------------

    def getGroups_kerning(self):
        groups = self.getGroups_generic()
        kerningGroups = {
            "public.kern1.A": ["A", "Aacute"],
            "public.kern1.O": ["O", "D"],
            "public.kern2.A": ["A", "Aacute"],
            "public.kern2.O": ["O", "C"]
        }
        groups.update(kerningGroups)
        return groups

    def test_side1KerningGroups(self):
        groups = self.getGroups_kerning()
        expected = {
            "public.kern1.A": ("A", "Aacute"),
            "public.kern1.O": ("O", "D")
        }
        self.assertEqual(groups.side1KerningGroups, expected)
        # self.assertEqual(super(groups, self)._get_side1KerningGroups(), expected)

    def test_get_side1KerningGroups(self):
        groups = self.getGroups_kerning()
        expected = {
            "public.kern1.A": ["A", "Aacute"],
            "public.kern1.O": ["O", "D"]
        }
        self.assertEqual(groups._get_side1KerningGroups(), expected)


    def test_side2KerningGroups(self):
        groups = self.getGroups_kerning()
        expected = {
            "public.kern2.A": ("A", "Aacute"),
            "public.kern2.O": ("O", "C")
        }
        self.assertEqual(groups.side2KerningGroups, expected)

    def test_get_side2KerningGroups(self):
        groups = self.getGroups_kerning()
        expected = {
            "public.kern1.A": ["A", "Aacute"],
            "public.kern1.O": ["O", "D"]
        }
        self.assertEqual(groups._get_side1KerningGroups(), expected)

    # ----
    # Hash
    # ----

    def test_hash(self):
        groups = self.getGroups_generic()
        self.assertEqual(
            isinstance(groups, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        groups_one = self.getGroups_generic()
        self.assertEqual(
            groups_one,
            groups_one
        )

    def test_object_not_equal_other(self):
        groups_one = self.getGroups_generic()
        groups_two = self.getGroups_generic()
        self.assertNotEqual(
            groups_one,
            groups_two
        )

    def test_object_equal_self_variable_assignment(self):
        groups_one = self.getGroups_generic()
        a = groups_one
        self.assertEqual(
            groups_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        groups_one = self.getGroups_generic()
        groups_two = self.getGroups_generic()
        a = groups_one
        self.assertNotEqual(
            groups_two,
            a
        )

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def test_remove(self):
        groups = self.getGroups_generic()
        groups.remove("group 2")
        expected = {
            "group 1": ("A", "B", "C"),
            "group 3": (),
            "group 4": ('A',)
        }
        self.assertEqual(groups.asDict(), expected)

    def test_remove_twice(self):
        groups = self.getGroups_generic()
        groups.remove("group 1")
        with self.assertRaises(KeyError):
            groups.remove("group 1")

    def test_remove_nonexistant_group(self):
        groups = self.getGroups_generic()
        with self.assertRaises(KeyError):
            groups.remove("group 7")

    def test_asDict(self):
        groups = self.getGroups_generic()
        expected = {
            "group 1": ("A", "B", "C"),
            "group 2": ("x", "y", "z"),
            "group 3": (),
            "group 4": ('A',)
        }
        self.assertEqual(groups.asDict(), expected)

    # -------------------
    # Inherited Functions
    # -------------------

    def test_iter(self):
        groups = self.getGroups_generic()
        expected = ["group 1","group 2","group 3", "group 4"]

        listOfGroups = []
        for groupName in groups:
            listOfGroups.append(groupName)

        self.assertEqual(listOfGroups.sort(), expected.sort())

    def test_iter_remove(self):
        groups = self.getGroups_generic()
        expected = []

        for groupName in groups:
            groups.remove(groupName)

        self.assertEqual(groups.keys(), expected)


    def test_values(self):
        groups = self.getGroups_generic()
        expected = [("A", "B", "C"), ("x", "y", "z"),(),('A',)]
        self.assertEqual(groups.values().sort(), expected.sort())
