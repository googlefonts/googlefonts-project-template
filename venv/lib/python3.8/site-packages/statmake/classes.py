import enum
import functools
import os
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Set, Tuple, Union

import attr
import cattr
import fontTools.designspaceLib
import fontTools.misc.plistlib

from .errors import StylespaceError

DESIGNSPACE_STYLESPACE_INLINE_KEY = "org.statmake.stylespace"
DESIGNSPACE_STYLESPACE_PATH_KEY = "org.statmake.stylespacePath"


class AxisValueFlag(enum.Flag):
    OlderSiblingFontAttribute = 0x0001
    ElidableAxisValueName = 0x0002


@attr.s(auto_attribs=True, frozen=True, slots=True)
class FlagList:
    """Represent a list of AxisValueFlags so I can implement a value
    property."""

    flags: List[AxisValueFlag] = attr.ib(factory=list)

    @property
    def value(self) -> int:
        """Return the value of all flags ORed together."""
        if not self.flags:
            return 0
        return functools.reduce(lambda x, y: x | y, self.flags).value


@attr.s(auto_attribs=True, frozen=True, slots=True)
class NameRecord:
    """Represent a IETF BCP 47 language code to name string mapping for the
    `name` table."""

    mapping: Mapping[str, str]

    def __attrs_post_init__(self) -> None:
        if "en" not in self.mapping:
            raise StylespaceError(
                "All NameRecords must have a default English (IETF BCP 47 language "
                "code 'en') entry."
            )

    def __getitem__(self, key: str) -> str:
        return self.mapping.__getitem__(key)

    @property
    def default(self) -> str:
        return self.mapping["en"]

    @classmethod
    def from_string(cls, name: str) -> "NameRecord":
        return cls(mapping={"en": name})

    @classmethod
    def from_dict(cls, dictionary: Mapping) -> "NameRecord":
        return cls(mapping=dictionary)

    @classmethod
    def structure(cls, data: Union[str, dict]) -> "NameRecord":
        if isinstance(data, str):
            return cls.from_string(data)
        if isinstance(data, dict):
            return cls.from_dict(data)
        raise StylespaceError(f"Don't know how to construct NameRecord from '{data}'.")


@attr.s(auto_attribs=True, frozen=True, slots=True)
class LocationFormat1:
    name: NameRecord
    value: float
    flags: FlagList = attr.ib(factory=FlagList)

    def to_builder_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name.mapping,
            "value": self.value,
            "flags": self.flags.value,
        }


@attr.s(auto_attribs=True, frozen=True, slots=True)
class LocationFormat2:
    name: NameRecord
    value: float
    range: Tuple[float, float]
    flags: FlagList = attr.ib(factory=FlagList)

    def __attrs_post_init__(self) -> None:
        if len(self.range) != 2:
            raise StylespaceError("Range must be a value pair of (min, max).")

    def to_builder_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name.mapping,
            "nominalValue": self.value,
            "rangeMinValue": self.range[0],
            "rangeMaxValue": self.range[1],
            "flags": self.flags.value,
        }


@attr.s(auto_attribs=True, frozen=True, slots=True)
class LocationFormat3:
    name: NameRecord
    value: float
    linked_value: float
    flags: FlagList = attr.ib(factory=FlagList)

    def to_builder_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name.mapping,
            "value": self.value,
            "linkedValue": self.linked_value,
            "flags": self.flags.value,
        }


@attr.s(auto_attribs=True, frozen=True, slots=True)
class LocationFormat4:
    name: NameRecord
    axis_values: Mapping[str, float]
    flags: FlagList = attr.ib(factory=FlagList)

    def to_builder_dict(self, name_to_tag: Mapping[str, str]) -> Dict[str, Any]:
        return {
            "name": self.name.mapping,
            "location": {name_to_tag[k]: v for k, v in self.axis_values.items()},
            "flags": self.flags.value,
        }


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Axis:
    name: NameRecord
    tag: str
    locations: List[Union[LocationFormat1, LocationFormat2, LocationFormat3]] = attr.ib(
        factory=list
    )
    ordering: Optional[int] = None


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Stylespace:
    axes: List[Axis]
    locations: List[LocationFormat4] = attr.ib(factory=list)
    elided_fallback_name_id: int = 2

    def __attrs_post_init__(self) -> None:
        """Fill in a default ordering unless the user specified at least one
        custom one, also do sanity checking.

        This works around the frozen state with `object.__setattr__`.
        """
        if all(axis.ordering is None for axis in self.axes):
            for index, axis in enumerate(self.axes):
                object.__setattr__(axis, "ordering", index)
        elif not all(
            isinstance(axis.ordering, int) and axis.ordering >= 0 for axis in self.axes
        ):
            raise StylespaceError(
                "If you specify the ordering for one axis, you must specify all of "
                "them and they must be >= 0."
            )

        # Ensure named locations only contain axis names that are present in the
        # Stylespace and specify a location for all axes.
        available_axes = {a.name.default for a in self.axes}
        for named_location in self.locations:
            named_location_axes = set(named_location.axis_values.keys())
            if named_location_axes != available_axes:
                raise StylespaceError(
                    f"Location named '{named_location.name.default}' must specify "
                    "values for all axes in the Stylespace and contain no other axis "
                    "names."
                )

        # Ensure that all name records have the same languages specified.
        reference_languages = None
        for axis in self.axes:
            if reference_languages is None:
                reference_languages = sorted(axis.name.mapping.keys())
            for location in axis.locations:
                location_languages = sorted(location.name.mapping.keys())
                if location_languages != reference_languages:
                    raise StylespaceError(
                        "All names must be supplied in the same languages. On axis "
                        f"'{axis.name.default}', location '{location.name.default}' is "
                        f"named in languages {location_languages} but "
                        f"expected was {reference_languages}."
                    )
        for named_location in self.locations:
            assert reference_languages is not None
            location_languages = sorted(named_location.name.mapping.keys())
            if location_languages != reference_languages:
                raise StylespaceError(
                    "All names must be supplied in the same languages. The named "
                    f"location '{named_location.name.default}' is "
                    f"named in languages {location_languages} but "
                    f"expected was {reference_languages}."
                )

        # Ensure linked_values are present on the same axis in the Stylespace
        for axis in self.axes:
            values = {l.value for l in axis.locations}
            for location in axis.locations:
                linked_value: Optional[float] = getattr(location, "linked_value", None)
                if linked_value is not None and linked_value not in values:
                    raise StylespaceError(
                        f"On axis '{axis.name.default}', location "
                        f"'{location.name.default}' specifies a linked_value of "
                        f"'{linked_value}', which does not exist on that axis "
                        "(ranges are ignored)."
                    )

        # Ensure location values are unique.
        for axis in self.axes:
            values = set()
            for location in axis.locations:
                if location.value in values:
                    raise StylespaceError(
                        f"On axis '{axis.name.default}', location "
                        f"'{location.name.default}' specifies a duplicate location "
                        f"value of '{location.value}', which is already assigned on "
                        "the same axis."
                    )
                values.add(location.value)
        named_values: Set[Tuple[Tuple[str, float], ...]] = set()
        for named_location in self.locations:
            named_location_tuple = tuple(named_location.axis_values.items())
            if named_location_tuple in named_values:
                raise StylespaceError(
                    f"The named location '{named_location.name.default}' specifies a "
                    "duplicate location already taken by another."
                )
            named_values.add(named_location_tuple)

    @classmethod
    def from_dict(cls, dict_data: dict) -> "Stylespace":
        """Construct Stylespace from unstructured dict data."""
        converter = cattr.Converter()
        converter.register_structure_hook(
            FlagList,
            lambda list_of_str_flags, cls: cls(
                [getattr(AxisValueFlag, f) for f in list_of_str_flags]
            ),
        )
        converter.register_structure_hook(
            NameRecord, lambda data, cls: cls.structure(data)
        )
        return converter.structure(dict_data, cls)

    @classmethod
    def from_bytes(cls, stylespace_content: bytes) -> "Stylespace":
        """Construct Stylespace from bytes containing (XML) plist data."""
        stylespace_content_parsed = fontTools.misc.plistlib.loads(stylespace_content)
        return cls.from_dict(stylespace_content_parsed)

    @classmethod
    def from_file(cls, stylespace_path: Union[str, bytes, os.PathLike]) -> "Stylespace":
        """Construct Stylespace from path to (XML) plist file."""
        with open(stylespace_path, "rb") as fp:
            return cls.from_bytes(fp.read())

    @classmethod
    def from_designspace(
        cls, designspace: fontTools.designspaceLib.DesignSpaceDocument
    ) -> "Stylespace":
        f"""Construct Stylespace from unstructured dict data or a path stored in a
        Designspace object's lib.

        The keys:

        - `{DESIGNSPACE_STYLESPACE_INLINE_KEY}`: The content of a regular Stylespace
          file as a dict.
        - `{DESIGNSPACE_STYLESPACE_PATH_KEY}`: A path to an external Stylespace file,
          relative to the Designspace file (the Designspace object must have the `path`
          attribute set).
        """
        stylespace_inline = designspace.lib.get(DESIGNSPACE_STYLESPACE_INLINE_KEY)
        stylespace_path = designspace.lib.get(DESIGNSPACE_STYLESPACE_PATH_KEY)

        if (stylespace_inline and stylespace_path) or (
            not stylespace_inline and not stylespace_path
        ):
            raise StylespaceError(
                "Designspace lib must contain EITHER inline Stylespace data OR a path "
                "to an external Stylespace file."
            )

        if stylespace_inline:
            return cls.from_dict(stylespace_inline)

        if not designspace.path:
            raise StylespaceError(
                "Designspace object must have `path` attribute set, because the "
                "Stylespace path is relative to the Designspace file."
            )
        stylespace_path_lookup = Path(designspace.path).parent / stylespace_path
        return cls.from_file(stylespace_path_lookup)
