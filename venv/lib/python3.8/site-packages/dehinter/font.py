# Copyright 2019 Source Foundry Authors and Contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import array
import os
import pprint
import sys
from typing import Union

from fontTools import ttLib  # type: ignore

from dehinter.bitops import clear_bit_k, is_bit_k_set

# instantiate pretty printer
pp = pprint.PrettyPrinter(indent=4)


def _report_actions(table, has_table):
    if not has_table:
        print(f"[-] Removed {table} table")
    else:  # pragma: no cover
        sys.stderr.write(
            f"[!] Error: failed to remove {table} table from font{os.linesep}"
        )


# ========================================================
# Core dehinting routine
# ========================================================
def dehint(
    tt,
    keep_cvar=False,
    keep_cvt=False,
    keep_fpgm=False,
    keep_gasp=False,
    keep_glyf=False,
    keep_hdmx=False,
    keep_head=False,
    keep_ltsh=False,
    keep_maxp=False,
    keep_prep=False,
    keep_ttfa=False,
    keep_vdmx=False,
    verbose=True,
):

    if is_variable_font(tt) and not keep_cvar:
        if has_cvar_table(tt):
            remove_cvar_table(tt)
            if verbose:
                _report_actions("cvar", has_cvar_table(tt))

    if not keep_cvt:
        if has_cvt_table(tt):
            remove_cvt_table(tt)
            if verbose:
                _report_actions("cvt", has_cvt_table(tt))

    if not keep_fpgm:
        if has_fpgm_table(tt):
            remove_fpgm_table(tt)
            if verbose:
                _report_actions("fpgm", has_fpgm_table(tt))

    if not keep_hdmx:
        if has_hdmx_table(tt):
            remove_hdmx_table(tt)
            if verbose:
                _report_actions("hdmx", has_hdmx_table(tt))

    if not keep_ltsh:
        if has_ltsh_table(tt):
            remove_ltsh_table(tt)
            if verbose:
                _report_actions("LTSH", has_ltsh_table(tt))

    if not keep_prep:
        if has_prep_table(tt):
            remove_prep_table(tt)
            if verbose:
                _report_actions("prep", has_prep_table(tt))

    if not keep_ttfa:
        if has_ttfa_table(tt):
            remove_ttfa_table(tt)
            if verbose:
                _report_actions("ttfa", has_ttfa_table(tt))

    if not keep_vdmx:
        if has_vdmx_table(tt):
            remove_vdmx_table(tt)
            if verbose:
                _report_actions("VDMX", has_vdmx_table(tt))

    #  (2) Remove glyf table instruction set bytecode
    if not keep_glyf:
        number_glyfs_edited = remove_glyf_instructions(tt)
        if number_glyfs_edited > 0:
            if verbose:
                print(
                    f"[-] Removed glyf table instruction bytecode from "
                    f"{number_glyfs_edited} glyphs"
                )

    #  (3) Edit gasp table
    if not keep_gasp:
        if update_gasp_table(tt):
            gasp_string = pp.pformat(tt["gasp"].__dict__)
            if verbose:
                print(f"[Δ] New gasp table values:{os.linesep}    {gasp_string}")

    #  (4) Edit maxp table
    if not keep_maxp:
        if update_maxp_table(tt):
            maxp_string = pp.pformat(tt["maxp"].__dict__)
            if verbose:
                print(f"[Δ] New maxp table values:{os.linesep}    {maxp_string}")

    #  (5) Edit head table flags to clear bit 4
    if not keep_head:
        if update_head_table_flags(tt):
            if verbose:
                print("[Δ] Cleared bit 4 in head table flags")


# ========================================================
# Utilities
# ========================================================
def has_cvar_table(tt) -> bool:
    """Tests for the presence of a cvat table in a TrueType variable font."""
    return "cvar" in tt


def has_cvt_table(tt) -> bool:
    """Tests for the presence of a cvt table in a TrueType font."""
    return "cvt " in tt


def has_fpgm_table(tt) -> bool:
    """Tests for the presence of a fpgm table in a TrueType font."""
    return "fpgm" in tt


def has_gasp_table(tt) -> bool:
    """Tests for the presence of a gasp table in a TrueType font."""
    return "gasp" in tt


def has_hdmx_table(tt) -> bool:
    """Tests for the presence of a hdmx table in a TrueType font."""
    return "hdmx" in tt


def has_ltsh_table(tt) -> bool:
    """Tests for the presence of a LTSH table in a TrueType font."""
    return "LTSH" in tt


def has_prep_table(tt) -> bool:
    """Tests for the presence of a prep table in a TrueType font."""
    return "prep" in tt


def has_ttfa_table(tt) -> bool:
    """Tests for the presence of a TTFA table in a TrueType font."""
    return "TTFA" in tt


def has_vdmx_table(tt) -> bool:
    """Tests for the presence of a VDMX table in a TrueType font."""
    return "VDMX" in tt


def is_truetype_font(filepath: Union[bytes, str, "os.PathLike[str]"]) -> bool:
    """Tests that a font has the TrueType file signature of either:
    1) b'\x00\x01\x00\x00'
    2) b'\x74\x72\x75\x65' == 'true'"""
    with open(filepath, "rb") as f:
        file_signature: bytes = f.read(4)

        return file_signature in (b"\x00\x01\x00\x00", b"\x74\x72\x75\x65")


def is_variable_font(tt) -> bool:
    """Tests for the presence of a fvar table to confirm that a file is
    a variable font."""
    return "fvar" in tt


# ========================================================
# OpenType table removal
# ========================================================
def remove_cvar_table(tt) -> None:
    """Removes cvt table from a fontTools.ttLib.TTFont object"""
    try:
        del tt["cvar"]
    except KeyError:
        # do nothing if table is not present in the font
        pass


def remove_cvt_table(tt) -> None:
    """Removes cvt table from a fontTools.ttLib.TTFont object"""
    try:
        del tt["cvt "]
    except KeyError:
        # do nothing if table is not present in the font
        pass


def remove_fpgm_table(tt) -> None:
    """Removes fpgm table from a fontTools.ttLib.TTFont object"""
    try:
        del tt["fpgm"]
    except KeyError:
        # do nothing if table is not present in the font
        pass


def remove_hdmx_table(tt) -> None:
    """Removes hdmx table from a fontTools.ttLib.TTFont object"""
    try:
        del tt["hdmx"]
    except KeyError:
        # do nothing if table is not present in the font
        pass


def remove_ltsh_table(tt) -> None:
    """Removes LTSH table from a fontTools.ttLib.TTFont object."""
    try:
        del tt["LTSH"]
    except KeyError:
        # do nothing if table is not present in the font
        pass


def remove_prep_table(tt) -> None:
    """Removes prep table from a fontTools.ttLib.TTFont object"""
    try:
        del tt["prep"]
    except KeyError:
        # do nothing if table is not present in the font
        pass


def remove_ttfa_table(tt) -> None:
    """Removes TTFA table from a fontTools.ttLib.TTFont object"""
    try:
        del tt["TTFA"]
    except KeyError:
        # do nothing if table is not present in the font
        pass


def remove_vdmx_table(tt) -> None:
    """Removes TTFA table from a fontTools.ttLib.TTFont object"""
    try:
        del tt["VDMX"]
    except KeyError:
        # do nothing if table is not present in the font
        pass


# ========================================================
# glyf table instruction set bytecode removal
# ========================================================
def remove_glyf_instructions(tt) -> int:
    """Removes instruction set bytecode from glyph definitions in the glyf table."""
    glyph_number: int = 0
    for glyph in tt["glyf"].glyphs.values():
        glyph.expand(tt["glyf"])
        if hasattr(glyph, "program") and glyph.program.bytecode != array.array("B", []):
            if glyph.isComposite():
                del glyph.program
                glyph_number += 1
            else:
                glyph.program.bytecode = array.array("B", [])
                glyph_number += 1
    return glyph_number


# ========================================================
# gasp table edit
# ========================================================
def update_gasp_table(tt) -> bool:
    """Modifies the following gasp table fields:
    1) rangeMaxPPEM changed to 65535
    2) rangeGaspBehavior changed to 0x000a (symmetric grayscale, no gridfit)"""
    if "gasp" not in tt:
        tt["gasp"] = ttLib.newTable("gasp")
        tt["gasp"].gaspRange = {}
    if tt["gasp"].gaspRange != {65535: 0x000A}:
        tt["gasp"].gaspRange = {65535: 0x000A}
        return True
    else:
        return False


# =========================================
# maxp table edits
# =========================================
def update_maxp_table(tt) -> bool:
    """Update the maxp table with new values based on elimination of instruction sets."""
    changed: bool = False
    if tt["maxp"].maxZones != 0:
        tt["maxp"].maxZones = 0
        changed = True
    if tt["maxp"].maxTwilightPoints != 0:
        tt["maxp"].maxTwilightPoints = 0
        changed = True
    if tt["maxp"].maxStorage != 0:
        tt["maxp"].maxStorage = 0
        changed = True
    if tt["maxp"].maxFunctionDefs != 0:
        tt["maxp"].maxFunctionDefs = 0
        changed = True
    if tt["maxp"].maxStackElements != 0:
        tt["maxp"].maxStackElements = 0
        changed = True
    if tt["maxp"].maxSizeOfInstructions != 0:
        tt["maxp"].maxSizeOfInstructions = 0
        changed = True
    return changed


# =========================================
# head table edits
# =========================================
def update_head_table_flags(tt) -> bool:
    if is_bit_k_set(tt["head"].flags, 4):
        # confirm that there is no LTSH or hdmx table
        # bit 4 should be set if either of these tables are present in font
        if has_hdmx_table(tt) or has_ltsh_table(tt):
            return False
        else:
            new_flags = clear_bit_k(tt["head"].flags, 4)
            tt["head"].flags = new_flags
            return True
    else:
        return False
