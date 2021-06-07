import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

import fontTools.designspaceLib
import fontTools.ttLib

import statmake
import statmake.classes
import statmake.lib
from statmake.errors import Error, StylespaceError


def main(args: Optional[List[str]] = None) -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=statmake.__version__,
    )
    parser.add_argument(
        "--stylespace",
        type=statmake.classes.Stylespace.from_file,
        help=(
            "The path to the Stylespace file, if it is not contained in the "
            "Designspace."
        ),
    )
    parser.add_argument(
        "--designspace",
        "-m",
        required=True,
        type=fontTools.designspaceLib.DesignSpaceDocument.fromfile,
        help="The path to the Designspace file used to generate the variable font.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        help="Write the modified font to this path instead of in-place.",
    )
    parser.add_argument(
        "variable_font", type=Path, help="The path to the variable font file."
    )
    parsed_args = parser.parse_args(args)
    designspace = parsed_args.designspace

    if parsed_args.stylespace:
        stylespace = parsed_args.stylespace
    else:
        try:
            stylespace = statmake.classes.Stylespace.from_designspace(designspace)
        except StylespaceError as e:
            logging.error("Could not load Stylespace data from Designspace: %s", str(e))
            sys.exit(1)
    additional_locations = designspace.lib.get("org.statmake.additionalLocations", {})

    font = fontTools.ttLib.TTFont(parsed_args.variable_font)
    try:
        statmake.lib.apply_stylespace_to_variable_font(
            stylespace, font, additional_locations
        )
    except Error as e:
        logging.error("Cannot apply Stylespace to font: %s", str(e))
        sys.exit(1)

    font.save(parsed_args.output_path or parsed_args.variable_font)
