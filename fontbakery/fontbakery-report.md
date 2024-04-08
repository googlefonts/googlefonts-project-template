## FontBakery report

fontbakery version: 0.11.2

<h2>Check results</h2><details><summary><b>[12] Rubik[wght].ttf</b></summary><div><details><summary>🔥 <b>FAIL:</b> Check license file has good copyright string. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/license/OFL_copyright">com.google.fonts/check/license/OFL_copyright</a>)</summary><div>


* 🔥 **FAIL** First line in license file is:

"copyright 20** the my font project authors (https://github.com/googlefonts/googlefonts-project-template)"

which does not match the expected format, similar to:

"Copyright 2022 The Familyname Project Authors (git url)" [code: bad-format]
</div></details><details><summary>⚠ <b>WARN:</b> Checking OS/2 achVendID. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/vendor_id">com.google.fonts/check/vendor_id</a>)</summary><div>


* ⚠ **WARN** OS/2 VendorID value 'NONE' is not yet recognized. If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at https://www.microsoft.com/typography/links/vendorlist.aspx
 [code: unknown]
</div></details><details><summary>⚠ <b>WARN:</b> Check for codepoints not covered by METADATA subsets. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/metadata/unreachable_subsetting">com.google.fonts/check/metadata/unreachable_subsetting</a>)</summary><div>


* ⚠ **WARN** The following codepoints supported by the font are not covered by
    any subsets defined in the font's metadata file, and will never
    be served. You can solve this by either manually adding additional
    subset declarations to METADATA.pb, or by editing the glyphset
    definitions.

 * U+02C7 CARON: try adding one of: yi, tifinagh, canadian-aboriginal
 * U+02D8 BREVE: try adding one of: yi, canadian-aboriginal
 * U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
 * U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
 * U+02DD DOUBLE ACUTE ACCENT: not included in any glyphset definition
 * U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, cherokee, tifinagh, coptic
 * U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
 * U+0307 COMBINING DOT ABOVE: try adding one of: old-permic, canadian-aboriginal, syriac, math, coptic, tai-le, malayalam, tifinagh
 * U+030A COMBINING RING ABOVE: try adding syriac
 * U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee
 * U+030C COMBINING CARON: try adding one of: tai-le, cherokee
 * U+0312 COMBINING TURNED COMMA ABOVE: not included in any glyphset definition
 * U+0326 COMBINING COMMA BELOW: not included in any glyphset definition
 * U+0327 COMBINING CEDILLA: not included in any glyphset definition
 * U+0328 COMBINING OGONEK: not included in any glyphset definition
 * U+0335 COMBINING SHORT STROKE OVERLAY: not included in any glyphset definition
 * U+0337 COMBINING SHORT SOLIDUS OVERLAY: not included in any glyphset definition
 * U+0338 COMBINING LONG SOLIDUS OVERLAY: not included in any glyphset definition
 * U+2021 DOUBLE DAGGER: try adding adlam
 * U+2030 PER MILLE SIGN: try adding adlam
 * U+2070 SUPERSCRIPT ZERO: not included in any glyphset definition
 * U+2075 SUPERSCRIPT FIVE: not included in any glyphset definition
 * U+2076 SUPERSCRIPT SIX: not included in any glyphset definition
 * U+2077 SUPERSCRIPT SEVEN: not included in any glyphset definition
 * U+2078 SUPERSCRIPT EIGHT: not included in any glyphset definition
 * U+2079 SUPERSCRIPT NINE: not included in any glyphset definition
 * U+207D SUPERSCRIPT LEFT PARENTHESIS: not included in any glyphset definition
 * U+207E SUPERSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition
 * U+2080 SUBSCRIPT ZERO: not included in any glyphset definition
 * U+2081 SUBSCRIPT ONE: not included in any glyphset definition
 * U+2082 SUBSCRIPT TWO: not included in any glyphset definition
 * U+2083 SUBSCRIPT THREE: not included in any glyphset definition
 * U+2084 SUBSCRIPT FOUR: not included in any glyphset definition
 * U+2085 SUBSCRIPT FIVE: not included in any glyphset definition
 * U+2086 SUBSCRIPT SIX: not included in any glyphset definition
 * U+2087 SUBSCRIPT SEVEN: not included in any glyphset definition
 * U+2088 SUBSCRIPT EIGHT: not included in any glyphset definition
 * U+2089 SUBSCRIPT NINE: not included in any glyphset definition
 * U+208D SUBSCRIPT LEFT PARENTHESIS: not included in any glyphset definition
 * U+208E SUBSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition
 * U+212E ESTIMATED SYMBOL: not included in any glyphset definition
 * U+2153 VULGAR FRACTION ONE THIRD: not included in any glyphset definition
 * U+2154 VULGAR FRACTION TWO THIRDS: not included in any glyphset definition
 * U+215B VULGAR FRACTION ONE EIGHTH: not included in any glyphset definition
 * U+215C VULGAR FRACTION THREE EIGHTHS: not included in any glyphset definition
 * U+215D VULGAR FRACTION FIVE EIGHTHS: not included in any glyphset definition
 * U+215E VULGAR FRACTION SEVEN EIGHTHS: not included in any glyphset definition
 * U+2202 PARTIAL DIFFERENTIAL: try adding math
 * U+2206 INCREMENT: try adding math
 * U+220F N-ARY PRODUCT: try adding math
 * U+2211 N-ARY SUMMATION: try adding math
 * U+221A SQUARE ROOT: try adding math
 * U+221E INFINITY: try adding math
 * U+222B INTEGRAL: try adding math
 * U+2248 ALMOST EQUAL TO: try adding math
 * U+2260 NOT EQUAL TO: try adding math
 * U+2264 LESS-THAN OR EQUAL TO: try adding math
 * U+2265 GREATER-THAN OR EQUAL TO: try adding math
 * U+25CA LOZENGE: try adding one of: math, symbols
 * U+FB01 LATIN SMALL LIGATURE FI: not included in any glyphset definition
 * U+FB02 LATIN SMALL LIGATURE FL: not included in any glyphset definition

Or you can add the above codepoints to one of the subsets supported by the font: `cyrillic`, `cyrillic-ext`, `greek-ext`, `hebrew`, `latin`, `latin-ext` [code: unreachable-subsetting]
</div></details><details><summary>⚠ <b>WARN:</b> Is there kerning info for non-ligated sequences? (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/kerning_for_non_ligated_sequences">com.google.fonts/check/kerning_for_non_ligated_sequences</a>)</summary><div>


* ⚠ **WARN** GPOS table lacks kerning info for the following non-ligated sequences:

	- f + f

	- f + i

	- i + f

	- f + l

	- l + f

	- i + l [code: lacks-kern-info]
</div></details><details><summary>⚠ <b>WARN:</b> Ensure fonts have ScriptLangTags declared on the 'meta' table. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/meta/script_lang_tags">com.google.fonts/check/meta/script_lang_tags</a>)</summary><div>


* ⚠ **WARN** This font file does not have a 'meta' table. [code: lacks-meta-table]
</div></details><details><summary>⚠ <b>WARN:</b> Check that legacy accents aren't used in composite glyphs. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/legacy_accents">com.google.fonts/check/legacy_accents</a>)</summary><div>


* ⚠ **WARN** Glyph "aacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "abreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni01CE" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "acircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "adieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "agrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "amacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "aring" has a legacy accent component  (ring). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "atilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "aeacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "cacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ccaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ccircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "cdotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "eacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ebreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ecaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ecircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "edieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "edotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "egrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "emacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gbreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gdotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "hcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "iacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ibreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "icircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "idieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "i.loclTRK" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "igrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "imacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "itilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni006A0301" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "jcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "lacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "nacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ncaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ntilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "oacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "obreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ocircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "odieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ograve" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ohungarumlaut" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "omacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "oslashacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "otilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "racute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "rcaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "sacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "scaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "scircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ubreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ucircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "udieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ugrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uhungarumlaut" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "umacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uring" has a legacy accent component  (ring). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "utilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wdieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wgrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "yacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ycircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ydieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ygrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "zacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "zcaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "zdotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0401" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0407" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04D2" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DC" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DE" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E2" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E4" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E6" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04EE" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F0" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F2" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F4" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F8" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0453" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0450" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0451" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni045D" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni045C" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0457" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04D3" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DD" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DF" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E3" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E5" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E7" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04EF" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F1" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F3" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F5" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F9" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0308" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0307" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gravecomb" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "acutecomb" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni030B" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0302" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni030C" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0306" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni030A" has a legacy accent component  (ring). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "tildecomb" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0304" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0327" has a legacy accent component  (cedilla). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0328" has a legacy accent component  (ogonek). It needs to be replaced by a combining mark. [code: legacy-accents-component]
</div></details><details><summary>⚠ <b>WARN:</b> Check font contains no unreachable glyphs (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/unreachable_glyphs">com.google.fonts/check/unreachable_glyphs</a>)</summary><div>


* ⚠ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

	- parenleft.denominator

	- parenleft.numerator

	- parenright.denominator

	- parenright.numerator

	- uni030C.alt
 [code: unreachable-glyphs]
</div></details><details><summary>⚠ <b>WARN:</b> Does the font contain a soft hyphen? (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/soft_hyphen">com.google.fonts/check/soft_hyphen</a>)</summary><div>


* ⚠ **WARN** This font has a 'Soft Hyphen' character. [code: softhyphen]
</div></details><details><summary>⚠ <b>WARN:</b> Check math signs have the same width. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/math_signs_width">com.google.fonts/check/math_signs_width</a>)</summary><div>


* ⚠ **WARN** The most common width is 527 among a set of 2 math glyphs.
The following math glyphs have a different width, though:

Width = 628:
plus

Width = 481:
less

Width = 571:
equal

Width = 480:
greater

Width = 581:
logicalnot

Width = 556:
plusminus

Width = 541:
multiply

Width = 565:
divide

Width = 650:
minus

Width = 563:
approxequal

Width = 545:
notequal
 [code: width-outliers]
</div></details><details><summary>⚠ <b>WARN:</b> Are there any misaligned on-curve points? (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/Outline Correctness Checks.html#com.google.fonts/check/outline_alignment_miss">com.google.fonts/check/outline_alignment_miss</a>)</summary><div>


* ⚠ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

	* parenleft (U+0028): X=204.0,Y=698.5 (should be at cap-height 700?)

	* parenright (U+0029): X=115.0,Y=698.5 (should be at cap-height 700?)

	* one (U+0031): X=263.0,Y=699.0 (should be at cap-height 700?)

	* at (U+0040): X=694.5,Y=-1.5 (should be at baseline 0?)

	* J (U+004A): X=196.0,Y=2.0 (should be at baseline 0?)

	* c (U+0063): X=353.5,Y=-0.5 (should be at baseline 0?)

	* braceright (U+007D): X=197.0,Y=699.5 (should be at cap-height 700?)

	* questiondown (U+00BF): X=97.0,Y=-2.0 (should be at baseline 0?)

	* aogonek (U+0105): X=445.0,Y=1.0 (should be at baseline 0?)

	* cacute (U+0107): X=353.5,Y=-0.5 (should be at baseline 0?)

	* ccircumflex (U+0109): X=353.5,Y=-0.5 (should be at baseline 0?)

	* cdotaccent (U+010B): X=353.5,Y=-0.5 (should be at baseline 0?)

	* ccaron (U+010D): X=353.5,Y=-0.5 (should be at baseline 0?)

	* eogonek (U+0119): X=213.0,Y=-2.0 (should be at baseline 0?)

	* Jcircumflex (U+0134): X=196.0,Y=2.0 (should be at baseline 0?)

	* uogonek (U+0173): X=485.0,Y=-2.0 (should be at baseline 0?)

	* uni0408 (U+0408): X=196.0,Y=2.0 (should be at baseline 0?)

	* uni0409 (U+0409): X=43.0,Y=1.0 (should be at baseline 0?)

	* uni0409 (U+0409): X=43.0,Y=1.0 (should be at baseline 0?)

	* uni0417 (U+0417): X=192.5,Y=698.5 (should be at cap-height 700?)

	* uni041B (U+041B): X=43.0,Y=1.0 (should be at baseline 0?)

	* uni0431 (U+0431): X=473.0,Y=702.0 (should be at cap-height 700?)

	* uni0441 (U+0441): X=353.5,Y=-0.5 (should be at baseline 0?)

	* uni0459 (U+0459): X=48.0,Y=1.0 (should be at baseline 0?)

	* uni0498 (U+0498): X=192.5,Y=698.5 (should be at cap-height 700?)

	* uni04AB (U+04AB): X=353.5,Y=-0.5 (should be at baseline 0?)

	* uni04DE (U+04DE): X=192.5,Y=698.5 (should be at cap-height 700?)

	* uni05E2 (U+05E2): X=62.0,Y=1.0 (should be at baseline 0?)

	* uni05EA (U+05EA): X=79.0,Y=2.0 (should be at baseline 0?)

	* uni2085 (U+2085): X=129.0,Y=-1.5 (should be at baseline 0?)

	* lozenge (U+25CA): X=227.5,Y=699.0 (should be at cap-height 700?)

	* lozenge (U+25CA): X=304.5,Y=699.0 (should be at cap-height 700?)

	* uniFB4A (U+FB4A): X=79.0,Y=2.0 (should be at baseline 0?) [code: found-misalignments]
</div></details><details><summary>⚠ <b>WARN:</b> Ensure dotted circle glyph is present and can attach marks. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/Shaping Checks.html#com.google.fonts/check/dotted_circle">com.google.fonts/check/dotted_circle</a>)</summary><div>


* ⚠ **WARN** No dotted circle glyph present [code: missing-dotted-circle]
</div></details><details><summary>⚠ <b>WARN:</b> Ensure soft_dotted characters lose their dot when combined with marks that replace the dot. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/Shaping Checks.html#com.google.fonts/check/soft_dotted">com.google.fonts/check/soft_dotted</a>)</summary><div>


* ⚠ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings: į̀ į́ į̂ į̃ į̄ į̌ і́

The dot of soft dotted characters _should_ disappear in other cases, for example: i̦̒ j̦̒ į̆ į̇ į̈ į̊ į̋ į̒ į̦̒ į̧̒ į̨̒ į̵̀ į̵́ į̵̂ į̵̃ į̵̄ į̵̆ į̵̇ į̵̈ į̵̊

Your font fully covers the following languages that require the soft-dotted feature: Belarusian (Cyrl, 10,064,517 speakers), Dutch (Latn, 31,709,104 speakers), Lithuanian (Latn, 2,357,094 speakers), Ukrainian (Cyrl, 29,273,587 speakers). 

Your font does *not* cover the following languages that require the soft-dotted feature: Lugbara (Latn, 2,200,000 speakers), Gulay (Latn, 250,478 speakers), Aghem (Latn, 38,843 speakers), South Central Banda (Latn, 244,000 speakers), Nzakara (Latn, 50,000 speakers), Mfumte (Latn, 79,000 speakers), Zapotec (Latn, 490,000 speakers), Igbo (Latn, 27,823,640 speakers), Ijo, Southeast (Latn, 2,471,000 speakers), Yala (Latn, 200,000 speakers), Basaa (Latn, 332,940 speakers), Nateni (Latn, 100,000 speakers), Ma’di (Latn, 584,000 speakers), Bafut (Latn, 158,146 speakers), Cicipu (Latn, 44,000 speakers), Makaa (Latn, 221,000 speakers), Kom (Latn, 360,685 speakers), Mundani (Latn, 34,000 speakers), Navajo (Latn, 166,319 speakers), Ebira (Latn, 2,200,000 speakers), Mango (Latn, 77,000 speakers), Dan (Latn, 1,099,244 speakers), Fur (Latn, 1,230,163 speakers), Sar (Latn, 500,000 speakers), Koonzime (Latn, 40,000 speakers), Ngbaka (Latn, 1,020,000 speakers), Kpelle, Guinea (Latn, 622,000 speakers), Southern Kisi (Latn, 360,000 speakers), Dii (Latn, 71,000 speakers), Ekpeye (Latn, 226,000 speakers), Ejagham (Latn, 120,000 speakers), Avokaya (Latn, 100,000 speakers), Bete-Bendi (Latn, 100,000 speakers). [code: soft-dotted]
</div></details><br></div></details><details><summary><b>[12] Rubik-Italic[wght].ttf</b></summary><div><details><summary>🔥 <b>FAIL:</b> Check license file has good copyright string. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/license/OFL_copyright">com.google.fonts/check/license/OFL_copyright</a>)</summary><div>


* 🔥 **FAIL** First line in license file is:

"copyright 20** the my font project authors (https://github.com/googlefonts/googlefonts-project-template)"

which does not match the expected format, similar to:

"Copyright 2022 The Familyname Project Authors (git url)" [code: bad-format]
</div></details><details><summary>⚠ <b>WARN:</b> Checking OS/2 achVendID. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/vendor_id">com.google.fonts/check/vendor_id</a>)</summary><div>


* ⚠ **WARN** OS/2 VendorID value 'NONE' is not yet recognized. If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at https://www.microsoft.com/typography/links/vendorlist.aspx
 [code: unknown]
</div></details><details><summary>⚠ <b>WARN:</b> Check for codepoints not covered by METADATA subsets. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/metadata/unreachable_subsetting">com.google.fonts/check/metadata/unreachable_subsetting</a>)</summary><div>


* ⚠ **WARN** The following codepoints supported by the font are not covered by
    any subsets defined in the font's metadata file, and will never
    be served. You can solve this by either manually adding additional
    subset declarations to METADATA.pb, or by editing the glyphset
    definitions.

 * U+02C7 CARON: try adding one of: yi, tifinagh, canadian-aboriginal
 * U+02D8 BREVE: try adding one of: yi, canadian-aboriginal
 * U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
 * U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
 * U+02DD DOUBLE ACUTE ACCENT: not included in any glyphset definition
 * U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, cherokee, tifinagh, coptic
 * U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
 * U+0307 COMBINING DOT ABOVE: try adding one of: old-permic, canadian-aboriginal, syriac, math, coptic, tai-le, malayalam, tifinagh
 * U+030A COMBINING RING ABOVE: try adding syriac
 * U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee
 * U+030C COMBINING CARON: try adding one of: tai-le, cherokee
 * U+0312 COMBINING TURNED COMMA ABOVE: not included in any glyphset definition
 * U+0326 COMBINING COMMA BELOW: not included in any glyphset definition
 * U+0327 COMBINING CEDILLA: not included in any glyphset definition
 * U+0328 COMBINING OGONEK: not included in any glyphset definition
 * U+0335 COMBINING SHORT STROKE OVERLAY: not included in any glyphset definition
 * U+0337 COMBINING SHORT SOLIDUS OVERLAY: not included in any glyphset definition
 * U+0338 COMBINING LONG SOLIDUS OVERLAY: not included in any glyphset definition
 * U+2021 DOUBLE DAGGER: try adding adlam
 * U+2030 PER MILLE SIGN: try adding adlam
 * U+2070 SUPERSCRIPT ZERO: not included in any glyphset definition
 * U+2075 SUPERSCRIPT FIVE: not included in any glyphset definition
 * U+2076 SUPERSCRIPT SIX: not included in any glyphset definition
 * U+2077 SUPERSCRIPT SEVEN: not included in any glyphset definition
 * U+2078 SUPERSCRIPT EIGHT: not included in any glyphset definition
 * U+2079 SUPERSCRIPT NINE: not included in any glyphset definition
 * U+207D SUPERSCRIPT LEFT PARENTHESIS: not included in any glyphset definition
 * U+207E SUPERSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition
 * U+2080 SUBSCRIPT ZERO: not included in any glyphset definition
 * U+2081 SUBSCRIPT ONE: not included in any glyphset definition
 * U+2082 SUBSCRIPT TWO: not included in any glyphset definition
 * U+2083 SUBSCRIPT THREE: not included in any glyphset definition
 * U+2084 SUBSCRIPT FOUR: not included in any glyphset definition
 * U+2085 SUBSCRIPT FIVE: not included in any glyphset definition
 * U+2086 SUBSCRIPT SIX: not included in any glyphset definition
 * U+2087 SUBSCRIPT SEVEN: not included in any glyphset definition
 * U+2088 SUBSCRIPT EIGHT: not included in any glyphset definition
 * U+2089 SUBSCRIPT NINE: not included in any glyphset definition
 * U+208D SUBSCRIPT LEFT PARENTHESIS: not included in any glyphset definition
 * U+208E SUBSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition
 * U+212E ESTIMATED SYMBOL: not included in any glyphset definition
 * U+2153 VULGAR FRACTION ONE THIRD: not included in any glyphset definition
 * U+2154 VULGAR FRACTION TWO THIRDS: not included in any glyphset definition
 * U+215B VULGAR FRACTION ONE EIGHTH: not included in any glyphset definition
 * U+215C VULGAR FRACTION THREE EIGHTHS: not included in any glyphset definition
 * U+215D VULGAR FRACTION FIVE EIGHTHS: not included in any glyphset definition
 * U+215E VULGAR FRACTION SEVEN EIGHTHS: not included in any glyphset definition
 * U+2202 PARTIAL DIFFERENTIAL: try adding math
 * U+2206 INCREMENT: try adding math
 * U+220F N-ARY PRODUCT: try adding math
 * U+2211 N-ARY SUMMATION: try adding math
 * U+221A SQUARE ROOT: try adding math
 * U+221E INFINITY: try adding math
 * U+222B INTEGRAL: try adding math
 * U+2248 ALMOST EQUAL TO: try adding math
 * U+2260 NOT EQUAL TO: try adding math
 * U+2264 LESS-THAN OR EQUAL TO: try adding math
 * U+2265 GREATER-THAN OR EQUAL TO: try adding math
 * U+25CA LOZENGE: try adding one of: math, symbols
 * U+FB01 LATIN SMALL LIGATURE FI: not included in any glyphset definition
 * U+FB02 LATIN SMALL LIGATURE FL: not included in any glyphset definition

Or you can add the above codepoints to one of the subsets supported by the font: `cyrillic`, `cyrillic-ext`, `greek-ext`, `hebrew`, `latin`, `latin-ext` [code: unreachable-subsetting]
</div></details><details><summary>⚠ <b>WARN:</b> Is there kerning info for non-ligated sequences? (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/kerning_for_non_ligated_sequences">com.google.fonts/check/kerning_for_non_ligated_sequences</a>)</summary><div>


* ⚠ **WARN** GPOS table lacks kerning info for the following non-ligated sequences:

	- f + f

	- f + i

	- i + f

	- f + l

	- l + f

	- i + l [code: lacks-kern-info]
</div></details><details><summary>⚠ <b>WARN:</b> Ensure fonts have ScriptLangTags declared on the 'meta' table. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/googlefonts.html#com.google.fonts/check/meta/script_lang_tags">com.google.fonts/check/meta/script_lang_tags</a>)</summary><div>


* ⚠ **WARN** This font file does not have a 'meta' table. [code: lacks-meta-table]
</div></details><details><summary>⚠ <b>WARN:</b> Check that legacy accents aren't used in composite glyphs. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/legacy_accents">com.google.fonts/check/legacy_accents</a>)</summary><div>


* ⚠ **WARN** Glyph "aacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "abreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni01CE" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "acircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "adieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "agrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "amacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "aring" has a legacy accent component  (ring). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "atilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "aeacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "cacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ccaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ccircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "cdotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "eacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ebreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ecaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ecircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "edieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "edotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "egrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "emacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gbreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gdotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "hcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "iacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ibreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "icircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "idieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "i.loclTRK" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "igrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "imacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "itilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni006A0301" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "jcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "lacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "nacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ncaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ntilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "oacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "obreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ocircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "odieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ograve" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ohungarumlaut" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "omacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "oslashacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "otilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "racute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "rcaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "sacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "scaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "scircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ubreve" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ucircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "udieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ugrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uhungarumlaut" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "umacron" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uring" has a legacy accent component  (ring). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "utilde" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wcircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wdieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "wgrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "yacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ycircumflex" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ydieresis" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "ygrave" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "zacute" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "zcaron" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "zdotaccent" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0401" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0407" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04D2" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DC" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DE" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E2" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E4" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E6" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04EE" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F0" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F4" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F8" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0453" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0450" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0451" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni045D" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni045C" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0457" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04D3" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DD" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04DF" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E3" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E5" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04E7" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04EF" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F1" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F3" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F5" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni04F9" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0308" has a legacy accent component  (dieresis). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0307" has a legacy accent component  (dotaccent). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "gravecomb" has a legacy accent component  (grave). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "acutecomb" has a legacy accent component  (acute). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni030B" has a legacy accent component  (hungarumlaut). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0302" has a legacy accent component  (circumflex). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni030C" has a legacy accent component  (caron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0306" has a legacy accent component  (breve). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni030A" has a legacy accent component  (ring). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "tildecomb" has a legacy accent component  (tilde). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0304" has a legacy accent component  (macron). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0327" has a legacy accent component  (cedilla). It needs to be replaced by a combining mark. [code: legacy-accents-component]
* ⚠ **WARN** Glyph "uni0328" has a legacy accent component  (ogonek). It needs to be replaced by a combining mark. [code: legacy-accents-component]
</div></details><details><summary>⚠ <b>WARN:</b> Check font contains no unreachable glyphs (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/unreachable_glyphs">com.google.fonts/check/unreachable_glyphs</a>)</summary><div>


* ⚠ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

	- parenleft.denominator

	- parenleft.numerator

	- parenright.denominator

	- parenright.numerator

	- uni030C.alt
 [code: unreachable-glyphs]
</div></details><details><summary>⚠ <b>WARN:</b> Does the font contain a soft hyphen? (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/soft_hyphen">com.google.fonts/check/soft_hyphen</a>)</summary><div>


* ⚠ **WARN** This font has a 'Soft Hyphen' character. [code: softhyphen]
</div></details><details><summary>⚠ <b>WARN:</b> Check math signs have the same width. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/universal.html#com.google.fonts/check/math_signs_width">com.google.fonts/check/math_signs_width</a>)</summary><div>


* ⚠ **WARN** The most common width is 527 among a set of 2 math glyphs.
The following math glyphs have a different width, though:

Width = 622:
plus

Width = 481:
less

Width = 574:
equal

Width = 480:
greater

Width = 585:
logicalnot

Width = 553:
plusminus

Width = 537:
multiply

Width = 561:
divide

Width = 652:
minus

Width = 563:
approxequal

Width = 540:
notequal
 [code: width-outliers]
</div></details><details><summary>⚠ <b>WARN:</b> Are there any misaligned on-curve points? (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/Outline Correctness Checks.html#com.google.fonts/check/outline_alignment_miss">com.google.fonts/check/outline_alignment_miss</a>)</summary><div>


* ⚠ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

	* parenleft (U+0028): X=288.0,Y=698.5 (should be at cap-height 700?)

	* parenright (U+0029): X=199.0,Y=698.0 (should be at cap-height 700?)

	* one (U+0031): X=342.0,Y=699.0 (should be at cap-height 700?)

	* at (U+0040): X=645.0,Y=-1.5 (should be at baseline 0?)

	* J (U+004A): X=140.5,Y=2.0 (should be at baseline 0?)

	* m (U+006D): X=266.5,Y=522.0 (should be at x-height 520?)

	* braceright (U+007D): X=296.5,Y=699.5 (should be at cap-height 700?)

	* questiondown (U+00BF): X=197.0,Y=-2.0 (should be at baseline 0?)

	* oslash (U+00F8): X=15.0,Y=1.0 (should be at baseline 0?)

	* aogonek (U+0105): X=326.0,Y=2.0 (should be at baseline 0?)

	* ccaron (U+010D): X=232.0,Y=699.0 (should be at cap-height 700?)

	* eogonek (U+0119): X=164.0,Y=-2.0 (should be at baseline 0?)

	* ecaron (U+011B): X=246.0,Y=699.0 (should be at cap-height 700?)

	* Jcircumflex (U+0134): X=140.5,Y=2.0 (should be at baseline 0?)

	* ncaron (U+0148): X=254.0,Y=699.0 (should be at cap-height 700?)

	* rcaron (U+0159): X=155.0,Y=699.0 (should be at cap-height 700?)

	* scaron (U+0161): X=200.0,Y=699.0 (should be at cap-height 700?)

	* uogonek (U+0173): X=436.0,Y=-2.0 (should be at baseline 0?)

	* zcaron (U+017E): X=200.0,Y=699.0 (should be at cap-height 700?)

	* uni01CE (U+01CE): X=228.0,Y=699.0 (should be at cap-height 700?)

	* oslashacute (U+01FF): X=15.0,Y=1.0 (should be at baseline 0?)

	* caron (U+02C7): X=35.0,Y=699.0 (should be at cap-height 700?)

	* uni030C (U+030C): X=35.0,Y=699.0 (should be at cap-height 700?)

	* uni0408 (U+0408): X=140.5,Y=2.0 (should be at baseline 0?)

	* uni0409 (U+0409): X=-31.0,Y=1.0 (should be at baseline 0?)

	* uni0409 (U+0409): X=-31.0,Y=1.0 (should be at baseline 0?)

	* uni0417 (U+0417): X=258.5,Y=698.5 (should be at cap-height 700?)

	* uni041B (U+041B): X=-31.0,Y=1.0 (should be at baseline 0?)

	* uni0431 (U+0431): X=552.0,Y=702.0 (should be at cap-height 700?)

	* uni0434 (U+0434): X=282.5,Y=698.5 (should be at cap-height 700?)

	* uni0459 (U+0459): X=-7.0,Y=1.0 (should be at baseline 0?)

	* uni0474 (U+0474): X=724.5,Y=701.5 (should be at cap-height 700?)

	* uni0498 (U+0498): X=258.5,Y=698.5 (should be at cap-height 700?)

	* uni04DE (U+04DE): X=258.5,Y=698.5 (should be at cap-height 700?)

	* uni05E2 (U+05E2): X=13.0,Y=1.0 (should be at baseline 0?)

	* uni05EA (U+05EA): X=31.0,Y=2.0 (should be at baseline 0?)

	* quoteright (U+2019): X=252.0,Y=701.5 (should be at cap-height 700?)

	* quotedblright (U+201D): X=252.0,Y=701.5 (should be at cap-height 700?)

	* quotedblright (U+201D): X=386.0,Y=701.5 (should be at cap-height 700?)

	* uni2085 (U+2085): X=80.0,Y=-1.5 (should be at baseline 0?)

	* lozenge (U+25CA): X=312.5,Y=701.5 (should be at cap-height 700?)

	* lozenge (U+25CA): X=387.5,Y=699.5 (should be at cap-height 700?)

	* uniFB2A (U+FB2A): X=718.5,Y=699.0 (should be at cap-height 700?)

	* uniFB2B (U+FB2B): X=241.5,Y=699.0 (should be at cap-height 700?)

	* uniFB2C (U+FB2C): X=718.5,Y=699.0 (should be at cap-height 700?)

	* uniFB2D (U+FB2D): X=241.5,Y=699.0 (should be at cap-height 700?)

	* uniFB4A (U+FB4A): X=31.0,Y=2.0 (should be at baseline 0?)

	* uniFB4B (U+FB4B): X=243.5,Y=699.0 (should be at cap-height 700?) [code: found-misalignments]
</div></details><details><summary>⚠ <b>WARN:</b> Ensure dotted circle glyph is present and can attach marks. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/Shaping Checks.html#com.google.fonts/check/dotted_circle">com.google.fonts/check/dotted_circle</a>)</summary><div>


* ⚠ **WARN** No dotted circle glyph present [code: missing-dotted-circle]
</div></details><details><summary>⚠ <b>WARN:</b> Ensure soft_dotted characters lose their dot when combined with marks that replace the dot. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/Shaping Checks.html#com.google.fonts/check/soft_dotted">com.google.fonts/check/soft_dotted</a>)</summary><div>


* ⚠ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings: į̀ į́ į̂ į̃ į̄ į̌ і́

The dot of soft dotted characters _should_ disappear in other cases, for example: i̦̒ j̦̒ į̆ į̇ į̈ į̊ į̋ į̒ į̦̒ į̧̒ į̨̒ į̵̀ į̵́ į̵̂ į̵̃ į̵̄ į̵̆ į̵̇ į̵̈ į̵̊

Your font fully covers the following languages that require the soft-dotted feature: Belarusian (Cyrl, 10,064,517 speakers), Dutch (Latn, 31,709,104 speakers), Lithuanian (Latn, 2,357,094 speakers), Ukrainian (Cyrl, 29,273,587 speakers). 

Your font does *not* cover the following languages that require the soft-dotted feature: Lugbara (Latn, 2,200,000 speakers), Gulay (Latn, 250,478 speakers), Aghem (Latn, 38,843 speakers), South Central Banda (Latn, 244,000 speakers), Nzakara (Latn, 50,000 speakers), Mfumte (Latn, 79,000 speakers), Zapotec (Latn, 490,000 speakers), Igbo (Latn, 27,823,640 speakers), Ijo, Southeast (Latn, 2,471,000 speakers), Yala (Latn, 200,000 speakers), Basaa (Latn, 332,940 speakers), Nateni (Latn, 100,000 speakers), Ma’di (Latn, 584,000 speakers), Bafut (Latn, 158,146 speakers), Cicipu (Latn, 44,000 speakers), Makaa (Latn, 221,000 speakers), Kom (Latn, 360,685 speakers), Mundani (Latn, 34,000 speakers), Navajo (Latn, 166,319 speakers), Ebira (Latn, 2,200,000 speakers), Mango (Latn, 77,000 speakers), Dan (Latn, 1,099,244 speakers), Fur (Latn, 1,230,163 speakers), Sar (Latn, 500,000 speakers), Koonzime (Latn, 40,000 speakers), Ngbaka (Latn, 1,020,000 speakers), Kpelle, Guinea (Latn, 622,000 speakers), Southern Kisi (Latn, 360,000 speakers), Dii (Latn, 71,000 speakers), Ekpeye (Latn, 226,000 speakers), Ejagham (Latn, 120,000 speakers), Avokaya (Latn, 100,000 speakers), Bete-Bendi (Latn, 100,000 speakers). [code: soft-dotted]
</div></details><br></div></details><details><summary><b>[1] Family checks</b></summary><div><details><summary>⚠ <b>WARN:</b> Make sure all font files have the same version value. (<a href="https://font-bakery.readthedocs.io/en/stable/fontbakery/profiles/head.html#com.google.fonts/check/family/equal_font_versions">com.google.fonts/check/family/equal_font_versions</a>)</summary><div>


* ⚠ **WARN** Version info differs among font files of the same font project.
These were the version values found:
* fonts/variable/Rubik[wght].ttf: 2.10400390625
* fonts/variable/Rubik-Italic[wght].ttf: 2.1020050048828125
 [code: mismatch]
</div></details><br></div></details>

### Summary

| 💔 ERROR | ☠ FATAL | 🔥 FAIL | ⚠ WARN | 💤 SKIP | ℹ INFO | 🍞 PASS | 🔎 DEBUG |
|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 0 | 0 | 2 | 23 | 205 | 17 | 254 | 0 |
| 0% | 0% | 0% | 5% | 41% | 3% | 51% | 0% |

**Note:** The following loglevels were omitted in this report:
* **SKIP**
* **INFO**
* **PASS**
* **DEBUG**
