"""
A set of objects that are suited to being the basis
of font development tools. This works on UFO files.
"""
from __future__ import absolute_import

try:
    from ._version import __version__
except ImportError:
    try:
        from setuptools_scm import get_version
        __version__ = get_version()
    except ImportError:
        __version__ = 'unknown'

from defcon.errors import DefconError

from defcon.objects.font import Font
from defcon.objects.layerSet import LayerSet
from defcon.objects.layer import Layer
from defcon.objects.glyph import Glyph, addRepresentationFactory, removeRepresentationFactory
from defcon.objects.contour import Contour
from defcon.objects.point import Point
from defcon.objects.component import Component
from defcon.objects.anchor import Anchor
from defcon.objects.image import Image
from defcon.objects.info import Info
from defcon.objects.groups import Groups
from defcon.objects.kerning import Kerning
from defcon.objects.features import Features
from defcon.objects.lib import Lib
from defcon.objects.uniData import UnicodeData
from defcon.objects.color import Color
from defcon.objects.guideline import Guideline
from defcon.objects.layoutEngine import LayoutEngine

def registerRepresentationFactory(cls, name, factory, destructiveNotifications=None):
    """
    Register **factory** as a representation factory
    for all instances of **cls** (a :class:`defcon.objects.base.BaseObject`)
    subclass under **name**.
    """
    if destructiveNotifications is None:
        destructiveNotifications = [cls.changeNotificationName]
    destructiveNotifications = set(destructiveNotifications)
    cls.representationFactories[name] = dict(factory=factory, destructiveNotifications=destructiveNotifications)

def unregisterRepresentationFactory(cls, name):
    """
    Unregister the representation factory stored under
    **name** in all instances of **cls**.
    """
    del cls.representationFactories[name]
