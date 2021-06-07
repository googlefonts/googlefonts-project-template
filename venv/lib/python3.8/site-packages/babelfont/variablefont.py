from babelfont.convertors.glyphs import _load_gsfont
from babelfont.convertors.ufo import load as load_ufo
from glyphsLib.builder.builders import UFOBuilder
from glyphsLib.classes import GSFont
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.varLib import models


class VariableFont:
    """An abstraction layer over the relationship between masters in a multiple
    master font environment. Practically, this means having access to masters
    (as Babelfont objects) and designspace objects, from either .glyphs or
    .designspace source files.


    Attributes:
        designspace: a ``fontTools.designspaceLib.DesignSpaceDocument`` instance.
        masters: a dictionary mapping master names to ``Babelfont.font`` objects.
        master_order: a list of the master names, in the order given in the source.
    """

    def __init__(self, filename=None):
        """Load a variable font from the given filename."""
        self.masters = {}
        self.designspace = None
        self.master_order = []
        if filename.endswith(".glyphs"):
            f = GSFont(filename)
            self.designspace = UFOBuilder(f).designspace
            self.masters = {master.name: _load_gsfont(master) for master in f.masters}
            self.master_order = [master.name for master in f.masters]
        elif filename.endswith(".designspace"):
            self.designspace = DesignSpaceDocument.fromfile(filename)
            self.designspace.loadSourceFonts(load_ufo)
            self.masters = {
                source.styleName: source.font for source in self.designspace.sources
            }
            self.master_order = [
                source.styleName for source in self.designspace.sources
            ]
        if self.designspace:
            self._make_model()

    def _make_model(self):
        masters = self.designspace.sources
        internal_master_locs = [o.location for o in masters]
        self.internal_axis_supports = {}
        for axis in self.designspace.axes:
            triple = (axis.minimum, axis.default, axis.maximum)
            self.internal_axis_supports[axis.name] = [
                axis.map_forward(v) for v in triple
            ]

        normalized_master_locs = [
            models.normalizeLocation(m, self.internal_axis_supports)
            for m in internal_master_locs
        ]
        axis_tags = [axis.name for axis in self.designspace.axes]
        self.variation_model = models.VariationModel(
            normalized_master_locs, axisOrder=axis_tags
        )

    def normalize(self, location):
        """Return a normalized location based on the designspace.

        Args:
            location:  A dictionary mapping axis names to user space coordinates.

        Example::

            >>> location = { "Width": 75, "Weight": 170 }
            >>> f.normalize(location)
            {'Weight': 0.8947368421052632, 'Width': -0.35714285714285715}
        """

        return models.normalizeLocation(location, self.internal_axis_supports)

    def interpolate_tuples(self, mastervalues, location, normalized=False):
        """Interpolates one or more values based on a location in the designspace.

        Args:
            mastervalues: A dictionary mapping master names to a value or tuple.
            location: A dictionary mapping axes to user space coordinates.
            normalized: True if the location is already normalized. Defaults to
                False.

        Example::
            >>> glyphs = [f.masters[master]["A"] for master in f.master_order]
            >>> widthset = {f.master_order[i]: glyphs[i].width for i in range(len(f.masters))}
            {'Light': 540, 'Light Condensed': 322, 'Condensed': 350, ... }
            >>> location = { "Width": 75, "Weight": 170 }
            >>>  f.interpolate_tuples(widthset, location)
            583.8504986842104
        """
        if not normalized:
            location = self.normalize(location)
        scalars = self.variation_model.getScalars(location)
        # The model expects each number to be an independent value, not
        # a tuple, whereas we would like to interpolate a bunch of stuff in
        # parallel.
        values = [mastervalues[x] for x in self.master_order]
        wastuples = isinstance(values[0], (list, tuple))
        values = [[x] if not wastuples else x for x in values]
        assert all(len(v) == len(values[0]) for v in values[1:])

        rv = [
            self.variation_model.interpolateFromDeltasAndScalars(
                self.variation_model.getDeltas(valueset), scalars
            )
            for valueset in zip(*values)
        ]
        if wastuples:
            return rv
        else:
            return rv[0]
