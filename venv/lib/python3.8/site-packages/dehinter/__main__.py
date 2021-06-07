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

import argparse
import os
import sys
from typing import List

from fontTools.ttLib import TTFont  # type: ignore

from dehinter import __version__
from dehinter.font import dehint, is_truetype_font
from dehinter.paths import filepath_exists, get_default_out_path
from dehinter.system import get_filesize


def main() -> None:  # pragma: no cover
    run(sys.argv[1:])


def run(argv: List[str]) -> None:
    # ===========================================================
    # argparse command line argument definitions
    # ===========================================================
    parser = argparse.ArgumentParser(
        description="A tool for the removal of TrueType instruction sets (hints) in fonts"
    )
    parser.add_argument(
        "--version", action="version", version="dehinter v{}".format(__version__)
    )
    parser.add_argument("-o", "--out", help="out file path (dehinted font)")
    parser.add_argument("--keep-cvar", help="keep cvar table", action="store_true")
    parser.add_argument("--keep-cvt", help="keep cvt table", action="store_true")
    parser.add_argument("--keep-fpgm", help="keep fpgm table", action="store_true")
    parser.add_argument("--keep-hdmx", help="keep hdmx table", action="store_true")
    parser.add_argument("--keep-ltsh", help="keep LTSH table", action="store_true")
    parser.add_argument("--keep-prep", help="keep prep table", action="store_true")
    parser.add_argument("--keep-ttfa", help="keep TTFA table", action="store_true")
    parser.add_argument("--keep-vdmx", help="keep VDMX table", action="store_true")
    parser.add_argument(
        "--keep-glyf", help="do not modify glyf table", action="store_true"
    )
    parser.add_argument(
        "--keep-gasp", help="do not modify gasp table", action="store_true"
    )
    parser.add_argument(
        "--keep-maxp", help="do not modify maxp table", action="store_true"
    )
    parser.add_argument(
        "--keep-head", help="do not modify head table", action="store_true"
    )
    parser.add_argument("--quiet", help="silence standard output", action="store_true")
    parser.add_argument("INFILE", help="in file path (hinted font)")

    args = parser.parse_args(argv)

    # ===========================================================
    # Command line logic
    # ===========================================================
    #
    # Validations
    # -----------
    #  (1) file path request is a file
    if not filepath_exists(args.INFILE):
        sys.stderr.write(
            f"[!] Error: '{args.INFILE}' is not a valid file path.{os.linesep}"
        )
        sys.stderr.write(f"[!] Request canceled.{os.linesep}")
        sys.exit(1)
    #  (2) the file is a ttf font file (based on the 4 byte file signature
    if not is_truetype_font(args.INFILE):
        sys.stderr.write(
            f"[!] Error: '{args.INFILE}' does not appear to be a TrueType font "
            f"file.{os.linesep}"
        )
        sys.stderr.write(f"[!] Request canceled.{os.linesep}")
        sys.exit(1)
    #   (3) confirm that out path is not the same as in path
    #    This tool does not support writing dehinted files in place over hinted version
    if args.INFILE == args.out:
        sys.stderr.write(
            f"[!] Error: You are attempting to overwrite the hinted file with the "
            f"dehinted file.  This is not supported. Please choose a different file "
            f"path for the dehinted file.{os.linesep}"
        )
        sys.exit(1)
    # Execution
    # ---------
    #  (1) OpenType table removal
    try:
        tt = TTFont(args.INFILE)
    except Exception as e:
        sys.stderr.write(
            f"[!] Error: Unable to create font object with '{args.INFILE}' -> {str(e)}"
        )
        sys.exit(1)

    use_verbose_output = not args.quiet

    dehint(
        tt,
        keep_cvar=args.keep_cvar,
        keep_cvt=args.keep_cvt,
        keep_fpgm=args.keep_fpgm,
        keep_gasp=args.keep_gasp,
        keep_glyf=args.keep_glyf,
        keep_hdmx=args.keep_hdmx,
        keep_head=args.keep_head,
        keep_ltsh=args.keep_ltsh,
        keep_maxp=args.keep_maxp,
        keep_prep=args.keep_prep,
        keep_ttfa=args.keep_ttfa,
        keep_vdmx=args.keep_vdmx,
        verbose=use_verbose_output,
    )

    # File write
    # ----------
    if args.out:
        # validation performed above to prevent this file path definition from
        # being the same as the in file path.  Write in place over a hinted
        # file is not supported
        outpath = args.out
    else:
        outpath = get_default_out_path(args.INFILE)

    try:
        tt.save(outpath)
        if use_verbose_output:
            print(f"{os.linesep}[+] Saved dehinted font as '{outpath}'")
    except Exception as e:  # pragma: no cover
        sys.stderr.write(
            f"[!] Error: Unable to save dehinted font file: {str(e)}{os.linesep}"
        )

    # File size comparison
    # --------------------
    if use_verbose_output:
        infile_size_tuple = get_filesize(args.INFILE)
        outfile_size_tuple = get_filesize(
            outpath
        )  # depends on outpath definition defined during file write
        print(f"{os.linesep}[*] File sizes:")
        print(f"    {infile_size_tuple[0]}{infile_size_tuple[1]} (hinted)")
        print(f"    {outfile_size_tuple[0]}{outfile_size_tuple[1]} (dehinted)")
