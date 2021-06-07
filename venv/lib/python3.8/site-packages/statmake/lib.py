import collections
from typing import Any, Dict, List, Mapping, Set, Tuple

import fontTools.otlLib.builder
import fontTools.ttLib

import statmake.classes
from statmake.errors import Error


def apply_stylespace_to_variable_font(
    stylespace: statmake.classes.Stylespace,
    varfont: fontTools.ttLib.TTFont,
    additional_locations: Mapping[str, float],
) -> None:
    """Generate and apply a STAT table to a variable font.

    additional_locations: used in subset Designspaces to express where on which other
    axes not defined by an <axis> element the varfont stands. The primary use-case is
    defining a complete STAT table for variable fonts that do not include all axes of a
    family (either because they intentionally contain just a subset of axes or because
    the designs are incompatible).
    """

    axes, locations, elided_fallback_name = _generate_builder_data(
        stylespace, varfont, additional_locations
    )
    fontTools.otlLib.builder.buildStatTable(
        varfont, axes, locations, elided_fallback_name
    )


def _generate_builder_data(
    stylespace: statmake.classes.Stylespace,
    varfont: fontTools.ttLib.TTFont,
    additional_locations: Mapping[str, float],
) -> Tuple[List[Mapping[str, Any]], List[Mapping[str, Any]], int]:
    """Generate axes and locations dictionaries for use in
    fontTools.otlLib.builder.buildStatTable, tailored to the font.

    Rules:
        1. There must be a fvar table so we know which named instances are defined.
            Every named instance needs a STAT entry for every point of its axis
            definition, i.e. an instance at {"Weight": 300, "Slant": 5} must have a
            Stylespace entry for Weight=300 and for Slant=5.
        2. The Stylespace must contain all axis names the varfont does and tags must
            match.
        3. Additional locations must only specify axes not in the font already and can
            only draw from axes available in the Stylespace.
        4. All name IDs must have a default English (United States) entry for the
            Windows platform, Unicode BMP encoding, to match axis names to tags.
        5. The font must get a location for every axis the Stylespace contains.
    """

    name_to_tag = {a.name.default: a.tag for a in stylespace.axes}
    _sanity_check(stylespace, varfont, additional_locations, name_to_tag)

    # First, determine which stops are used on which axes. The STAT table must contain
    # a name for each stop that is used on each axis, so each stop must have an entry
    # in the Stylespace. Also include locations in additional_locations that can refer
    # to axes not present in the current varfont.
    stylespace_stops: Dict[str, Set[float]] = {}
    for axis in stylespace.axes:
        stylespace_stops[axis.tag] = {l.value for l in axis.locations}
    for named_location in stylespace.locations:
        for name, value in named_location.axis_values.items():
            stylespace_stops[name_to_tag[name]].add(value)

    axis_stops: Mapping[str, Set[float]] = collections.defaultdict(set)  # tag to stops
    for instance in varfont["fvar"].instances:
        for k, v in instance.coordinates.items():
            if v not in stylespace_stops[k]:
                raise Error(
                    f"There is no Stylespace entry for stop {v} on the '{k}' axis."
                )
            axis_stops[k].add(v)

    for k, v in additional_locations.items():
        axis_tag = name_to_tag[k]
        if v not in stylespace_stops[axis_tag]:
            raise Error(
                f"There is no Stylespace entry for stop {v} on the '{k}' axis (from "
                "additional locations)."
            )
        axis_stops[axis_tag].add(v)

    # Generate formats 1, 2 and 3.
    builder_axes: List[Mapping[str, Any]] = [
        {
            "tag": axis.tag,
            "name": axis.name.mapping,
            "ordering": axis.ordering,
            "values": [
                location.to_builder_dict()
                for location in axis.locations
                if location.value in axis_stops[axis.tag]
            ],
        }
        for axis in stylespace.axes
    ]

    # Generate format 4.
    builder_locations: List[Mapping[str, Any]] = [
        named_location.to_builder_dict(name_to_tag)
        for named_location in stylespace.locations
        if all(
            name_to_tag[k] in axis_stops and v in axis_stops[name_to_tag[k]]
            for k, v in named_location.axis_values.items()
        )
    ]

    return builder_axes, builder_locations, stylespace.elided_fallback_name_id


def _sanity_check(
    stylespace: statmake.classes.Stylespace,
    varfont: fontTools.ttLib.TTFont,
    additional_locations: Mapping[str, float],
    stylespace_name_to_tag: Mapping[str, str],
) -> None:
    """Ensures the input data contains no obvious faults."""

    if "fvar" not in varfont:
        raise Error(
            "Need a variable font with the fvar table to determine which instances "
            "are present."
        )

    # Sanity check: only allow axis names in additional_locations that are present in
    # the Stylespace.
    stylespace_names_set = set(stylespace_name_to_tag.keys())
    additional_names_set = set(additional_locations.keys())
    if not additional_names_set.issubset(stylespace_names_set):
        surplus_keys = ", ".join(additional_names_set - stylespace_names_set)
        raise Error(
            "Additional locations must only contain axis names that are present in "
            f"the Stylespace, the following aren't: {surplus_keys}."
        )

    # Sanity check: Ensure all font axes are present in the Stylespace and tags match.
    font_name_to_tag = {
        _default_name_string(varfont, axis.axisNameID): axis.axisTag
        for axis in varfont["fvar"].axes
    }
    for name, tag in font_name_to_tag.items():
        if name not in stylespace_name_to_tag:
            raise Error(
                f"Font contains axis named '{name}' which is not in Stylespace. The "
                "Stylespace must contain all axes any font from the same family "
                "contains."
            )
        if stylespace_name_to_tag[name] != tag:
            raise Error(
                f"Font axis named '{name}' has tag '{tag}' but Stylespace defines it "
                f"to be '{stylespace_name_to_tag[name]}'. Axis names and tags must "
                "match between the font and the Stylespace."
            )

    # Sanity check: Only allow axis names in additional_locations that aren't in the
    # font already.
    for axis_name in additional_locations:
        if axis_name in font_name_to_tag:
            raise Error(
                f"Rejecting the additional location for the axis named '{axis_name}' "
                "because it is already present in the font."
            )

    # Sanity check: Ensure the location of the font is fully specified. This means
    # the font axis names plus additional_locations axis names must equal Stylespace
    # axis names.
    font_names_set = set(font_name_to_tag.keys()).union(additional_names_set)
    if font_names_set != stylespace_names_set:
        missing_axis_names = ", ".join(stylespace_names_set - font_names_set)
        raise Error(
            "The location of the font is not fully specified, missing locations "
            f"for the following axes: {missing_axis_names}."
        )


def _default_name_string(otfont: fontTools.ttLib.TTFont, name_id: int) -> str:
    """Return English name for name_id."""
    name = otfont["name"].getName(name_id, 3, 1, 0x409)
    if name is None:
        raise Error(f"No English record for id {name_id} for Windows platform.")
    return name.toStr()
