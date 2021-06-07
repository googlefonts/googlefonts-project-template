from __future__ import print_function
import sys
import unittest
from fontParts.test import test_normalizers
from fontParts.test import test_font
from fontParts.test import test_info
from fontParts.test import test_groups
from fontParts.test import test_kerning
from fontParts.test import test_features
from fontParts.test import test_layer
from fontParts.test import test_glyph
from fontParts.test import test_contour
from fontParts.test import test_segment
from fontParts.test import test_bPoint
from fontParts.test import test_point
from fontParts.test import test_component
from fontParts.test import test_anchor
from fontParts.test import test_image
from fontParts.test import test_lib
from fontParts.test import test_guideline
from fontParts.test import test_deprecated
from fontParts.test import test_color
from fontParts.test import test_world


def testEnvironment(objectGenerator, inApp=False, verbosity=1, testNormalizers=True):
    modules = [
        test_font,
        test_info,
        test_groups,
        test_kerning,
        test_features,
        test_layer,
        test_glyph,
        test_contour,
        test_segment,
        test_bPoint,
        test_point,
        test_component,
        test_anchor,
        test_image,
        test_lib,
        test_guideline,
        test_deprecated,
        test_color,
        test_world
    ]
    if testNormalizers:
        modules.append(test_normalizers)

    globalSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for module in modules:
        suite = loader.loadTestsFromModule(module)
        _setObjectGenerator(suite, objectGenerator)
        globalSuite.addTest(suite)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    succes = runner.run(globalSuite).wasSuccessful()
    if not inApp:
        sys.exit(not succes)
    else:
        return succes  # pragma: no cover


def _setObjectGenerator(suite, objectGenerator):
    for i in suite:
        if isinstance(i, unittest.TestSuite):
            _setObjectGenerator(i, objectGenerator)
        else:
            i.objectGenerator = objectGenerator
