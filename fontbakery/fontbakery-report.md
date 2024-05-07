## FontBakery report

fontbakery version: 0.12.5



## Experimental checks

These won't break the CI job for now, but will become effective after some time if nobody raises any concern.


<details><summary>[1] Rubik[wght].ttf</summary>
<div>
<details>
    <summary>⚠️ <b>WARN</b> Validate location, size and resolution of article images. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.article.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>Family metadata at fonts/variable does not have an article.</p>
 [code: lacks-article]



</div>
</details>
</div>
</details>

<details><summary>[1] Rubik-Italic[wght].ttf</summary>
<div>
<details>
    <summary>⚠️ <b>WARN</b> Validate location, size and resolution of article images. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.article.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>Family metadata at fonts/variable does not have an article.</p>
 [code: lacks-article]



</div>
</details>
</div>
</details>




## All other checks



<details><summary>[1] Family checks</summary>
<div>
<details>
    <summary>⚠️ <b>WARN</b> Make sure all font files have the same version value. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/opentype.head.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>Version info differs among font files of the same font project.
These were the version values found:</p>
<ul>
<li>fonts/variable/Rubik[wght].ttf: 2.10400390625</li>
<li>fonts/variable/Rubik-Italic[wght].ttf: 2.1020050048828125</li>
</ul>
 [code: mismatch]



</div>
</details>
</div>
</details>

<details><summary>[11] Rubik[wght].ttf</summary>
<div>
<details>
    <summary>🔥 <b>FAIL</b> Check license file has good copyright string. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.license.html#"></a></summary>
    <div>







* 🔥 **FAIL** <p>First line in license file is:</p>
<p>&quot;copyright 20** the my font project authors (<a href="https://github.com/googlefonts/googlefonts-project-template">https://github.com/googlefonts/googlefonts-project-template</a>)&quot;</p>
<p>which does not match the expected format, similar to:</p>
<p>&quot;Copyright 2022 The Familyname Project Authors (git url)&quot;</p>
 [code: bad-format]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check math signs have the same width. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The most common width is 527 among a set of 2 math glyphs.
The following math glyphs have a different width, though:</p>
<p>Width = 628:
plus</p>
<p>Width = 481:
less</p>
<p>Width = 571:
equal</p>
<p>Width = 480:
greater</p>
<p>Width = 581:
logicalnot</p>
<p>Width = 556:
plusminus</p>
<p>Width = 541:
multiply</p>
<p>Width = 565:
divide</p>
<p>Width = 650:
minus</p>
<p>Width = 563:
approxequal</p>
<p>Width = 545:
notequal</p>
 [code: width-outliers]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Does the font contain a soft hyphen? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>This font has a 'Soft Hyphen' character.</p>
 [code: softhyphen]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/outline.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have on-curve points which have potentially incorrect y coordinates:</p>
<pre><code>* J (U+004A): X=196.0,Y=2.0 (should be at baseline 0?)

* uni004A0301 (U+E001): X=196.0,Y=2.0 (should be at baseline 0?)

* Jcircumflex (U+0134): X=196.0,Y=2.0 (should be at baseline 0?)

* aogonek (U+0105): X=445.0,Y=1.0 (should be at baseline 0?)

* c (U+0063): X=353.5,Y=-0.5 (should be at baseline 0?)

* cacute (U+0107): X=353.5,Y=-0.5 (should be at baseline 0?)

* ccaron (U+010D): X=353.5,Y=-0.5 (should be at baseline 0?)

* ccircumflex (U+0109): X=353.5,Y=-0.5 (should be at baseline 0?)

* cdotaccent (U+010B): X=353.5,Y=-0.5 (should be at baseline 0?)

* eogonek (U+0119): X=213.0,Y=-2.0 (should be at baseline 0?)

* uogonek (U+0173): X=485.0,Y=-2.0 (should be at baseline 0?)

* uni0417 (U+0417): X=192.5,Y=698.5 (should be at cap-height 700?)

* uni041B (U+041B): X=43.0,Y=1.0 (should be at baseline 0?)

* uni0409 (U+0409): X=43.0,Y=1.0 (should be at baseline 0?)

* uni0409 (U+0409): X=43.0,Y=1.0 (should be at baseline 0?)

* uni0408 (U+0408): X=196.0,Y=2.0 (should be at baseline 0?)

* uni0498 (U+0498): X=192.5,Y=698.5 (should be at cap-height 700?)

* uni04DE (U+04DE): X=192.5,Y=698.5 (should be at cap-height 700?)

* uni0431 (U+0431): X=473.0,Y=702.0 (should be at cap-height 700?)

* uni0441 (U+0441): X=353.5,Y=-0.5 (should be at baseline 0?)

* uni0459 (U+0459): X=48.0,Y=1.0 (should be at baseline 0?)

* uni04AB (U+04AB): X=353.5,Y=-0.5 (should be at baseline 0?)

* uni05E2 (U+05E2): X=62.0,Y=1.0 (should be at baseline 0?)

* uni05EA (U+05EA): X=79.0,Y=2.0 (should be at baseline 0?)

* uniFB4A (U+FB4A): X=79.0,Y=2.0 (should be at baseline 0?)

* one (U+0031): X=263.0,Y=699.0 (should be at cap-height 700?)

* one.tf (U+E009): X=298.0,Y=699.0 (should be at cap-height 700?)

* five.dnom (U+E018): X=110.0,Y=1.5 (should be at baseline 0?)

* uni2085 (U+2085): X=129.0,Y=-1.5 (should be at baseline 0?)

* questiondown (U+00BF): X=97.0,Y=-2.0 (should be at baseline 0?)

* parenleft (U+0028): X=204.0,Y=698.5 (should be at cap-height 700?)

* parenright (U+0029): X=115.0,Y=698.5 (should be at cap-height 700?)

* braceright (U+007D): X=197.0,Y=699.5 (should be at cap-height 700?)

* at (U+0040): X=694.5,Y=-1.5 (should be at baseline 0?)

* lozenge (U+25CA): X=227.5,Y=699.0 (should be at cap-height 700?)

* lozenge (U+25CA): X=304.5,Y=699.0 (should be at cap-height 700?)
</code></pre>
 [code: found-misalignments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check the direction of the outermost contour in each glyph <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/outline.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have a counter-clockwise outer contour:</p>
<pre><code>* uni05B8 (U+05B8) has a counter-clockwise outer contour
</code></pre>
 [code: ccw-outer-contour]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Ensure dotted circle glyph is present and can attach marks. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/shaping.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>No dotted circle glyph present</p>
 [code: missing-dotted-circle]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that replace the dot. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/shaping.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The dot of soft dotted characters used in orthographies <em>must</em> disappear in the following strings: į̀ į́ į̂ į̃ į̄ į̌ і́</p>
<p>The dot of soft dotted characters <em>should</em> disappear in other cases, for example: i̦̒ j̦̒ į̆ į̇ į̈ į̊ į̋ į̒ į̦̒ į̧̒ į̨̒ į̵̀ į̵́ į̵̂ į̵̃ į̵̄ į̵̆ į̵̇ į̵̈ į̵̊</p>
<p>Your font fully covers the following languages that require the soft-dotted feature: Ukrainian (Cyrl, 29,273,587 speakers), Lithuanian (Latn, 2,357,094 speakers), Belarusian (Cyrl, 10,064,517 speakers), Dutch (Latn, 31,709,104 speakers).</p>
<p>Your font does <em>not</em> cover the following languages that require the soft-dotted feature: Zapotec (Latn, 490,000 speakers), Southern Kisi (Latn, 360,000 speakers), Ngbaka (Latn, 1,020,000 speakers), Makaa (Latn, 221,000 speakers), Nzakara (Latn, 50,000 speakers), Navajo (Latn, 166,319 speakers), Koonzime (Latn, 40,000 speakers), Avokaya (Latn, 100,000 speakers), Dii (Latn, 71,000 speakers), Ejagham (Latn, 120,000 speakers), Mango (Latn, 77,000 speakers), Nateni (Latn, 100,000 speakers), Mfumte (Latn, 79,000 speakers), Fur (Latn, 1,230,163 speakers), Cicipu (Latn, 44,000 speakers), Gulay (Latn, 250,478 speakers), Ijo, Southeast (Latn, 2,471,000 speakers), Kom (Latn, 360,685 speakers), Igbo (Latn, 27,823,640 speakers), Sar (Latn, 500,000 speakers), Basaa (Latn, 332,940 speakers), Ma’di (Latn, 584,000 speakers), South Central Banda (Latn, 244,000 speakers), Bafut (Latn, 158,146 speakers), Lugbara (Latn, 2,200,000 speakers), Yala (Latn, 200,000 speakers), Dan (Latn, 1,099,244 speakers), Vute (Latn, 21,000 speakers), Kpelle, Guinea (Latn, 622,000 speakers), Bete-Bendi (Latn, 100,000 speakers), Ebira (Latn, 2,200,000 speakers), Ekpeye (Latn, 226,000 speakers), Mundani (Latn, 34,000 speakers), Aghem (Latn, 38,843 speakers).</p>
 [code: soft-dotted]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.subsets.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The following codepoints supported by the font are not covered by
any subsets defined in the font's metadata file, and will never
be served. You can solve this by either manually adding additional
subset declarations to METADATA.pb, or by editing the glyphset
definitions.</p>
<ul>
<li>U+02C7 CARON: try adding one of: yi, canadian-aboriginal, tifinagh</li>
<li>U+02D8 BREVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02DB OGONEK: try adding one of: canadian-aboriginal, yi</li>
<li>U+02DD DOUBLE ACUTE ACCENT: not included in any glyphset definition</li>
<li>U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: coptic, cherokee, tifinagh, math</li>
<li>U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh</li>
<li>U+0307 COMBINING DOT ABOVE: try adding one of: math, canadian-aboriginal, old-permic, tai-le, tifinagh, coptic, syriac, malayalam</li>
<li>U+030A COMBINING RING ABOVE: try adding syriac</li>
<li>U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee</li>
<li>U+030C COMBINING CARON: try adding one of: cherokee, tai-le</li>
<li>U+0312 COMBINING TURNED COMMA ABOVE: not included in any glyphset definition</li>
<li>U+0326 COMBINING COMMA BELOW: not included in any glyphset definition</li>
<li>U+0327 COMBINING CEDILLA: not included in any glyphset definition</li>
<li>U+0328 COMBINING OGONEK: not included in any glyphset definition</li>
<li>U+0335 COMBINING SHORT STROKE OVERLAY: not included in any glyphset definition</li>
<li>U+0337 COMBINING SHORT SOLIDUS OVERLAY: not included in any glyphset definition</li>
<li>U+0338 COMBINING LONG SOLIDUS OVERLAY: not included in any glyphset definition</li>
<li>U+2021 DOUBLE DAGGER: try adding adlam</li>
<li>U+2030 PER MILLE SIGN: try adding adlam</li>
<li>U+2070 SUPERSCRIPT ZERO: not included in any glyphset definition</li>
<li>U+2075 SUPERSCRIPT FIVE: not included in any glyphset definition</li>
<li>U+2076 SUPERSCRIPT SIX: not included in any glyphset definition</li>
<li>U+2077 SUPERSCRIPT SEVEN: not included in any glyphset definition</li>
<li>U+2078 SUPERSCRIPT EIGHT: not included in any glyphset definition</li>
<li>U+2079 SUPERSCRIPT NINE: not included in any glyphset definition</li>
<li>U+207D SUPERSCRIPT LEFT PARENTHESIS: not included in any glyphset definition</li>
<li>U+207E SUPERSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition</li>
<li>U+2080 SUBSCRIPT ZERO: not included in any glyphset definition</li>
<li>U+2081 SUBSCRIPT ONE: not included in any glyphset definition</li>
<li>U+2082 SUBSCRIPT TWO: not included in any glyphset definition</li>
<li>U+2083 SUBSCRIPT THREE: not included in any glyphset definition</li>
<li>U+2084 SUBSCRIPT FOUR: not included in any glyphset definition</li>
<li>U+2085 SUBSCRIPT FIVE: not included in any glyphset definition</li>
<li>U+2086 SUBSCRIPT SIX: not included in any glyphset definition</li>
<li>U+2087 SUBSCRIPT SEVEN: not included in any glyphset definition</li>
<li>U+2088 SUBSCRIPT EIGHT: not included in any glyphset definition</li>
<li>U+2089 SUBSCRIPT NINE: not included in any glyphset definition</li>
<li>U+208D SUBSCRIPT LEFT PARENTHESIS: not included in any glyphset definition</li>
<li>U+208E SUBSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition</li>
<li>U+212E ESTIMATED SYMBOL: not included in any glyphset definition</li>
<li>U+2153 VULGAR FRACTION ONE THIRD: not included in any glyphset definition</li>
<li>U+2154 VULGAR FRACTION TWO THIRDS: not included in any glyphset definition</li>
<li>U+215B VULGAR FRACTION ONE EIGHTH: not included in any glyphset definition</li>
<li>U+215C VULGAR FRACTION THREE EIGHTHS: not included in any glyphset definition</li>
<li>U+215D VULGAR FRACTION FIVE EIGHTHS: not included in any glyphset definition</li>
<li>U+215E VULGAR FRACTION SEVEN EIGHTHS: not included in any glyphset definition</li>
<li>U+2202 PARTIAL DIFFERENTIAL: try adding math</li>
<li>U+2206 INCREMENT: try adding math</li>
<li>U+220F N-ARY PRODUCT: try adding math</li>
<li>U+2211 N-ARY SUMMATION: try adding math</li>
<li>U+221A SQUARE ROOT: try adding math</li>
<li>U+221E INFINITY: try adding math</li>
<li>U+222B INTEGRAL: try adding math</li>
<li>U+2248 ALMOST EQUAL TO: try adding math</li>
<li>U+2260 NOT EQUAL TO: try adding math</li>
<li>U+2264 LESS-THAN OR EQUAL TO: try adding math</li>
<li>U+2265 GREATER-THAN OR EQUAL TO: try adding math</li>
<li>U+25CA LOZENGE: try adding one of: math, symbols</li>
<li>U+FB01 LATIN SMALL LIGATURE FI: not included in any glyphset definition</li>
<li>U+FB02 LATIN SMALL LIGATURE FL: not included in any glyphset definition</li>
</ul>
<p>Or you can add the above codepoints to one of the subsets supported by the font: <code>cyrillic</code>, <code>cyrillic-ext</code>, <code>greek-ext</code>, <code>hebrew</code>, <code>latin</code>, <code>latin-ext</code></p>
 [code: unreachable-subsetting]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Is there kerning info for non-ligated sequences? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.gpos.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>GPOS table lacks kerning info for the following non-ligated sequences:</p>
<pre><code>- f + f

- f + i

- f + l
</code></pre>
 [code: lacks-kern-info]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Ensure fonts have ScriptLangTags declared on the 'meta' table. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.meta.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>This font file does not have a 'meta' table.</p>
 [code: lacks-meta-table]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Checking OS/2 achVendID. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.os2.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>OS/2 VendorID value 'NONE' is not yet recognized. If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at <a href="https://www.microsoft.com/typography/links/vendorlist.aspx">https://www.microsoft.com/typography/links/vendorlist.aspx</a></p>
 [code: unknown]



</div>
</details>
</div>
</details>

<details><summary>[11] Rubik-Italic[wght].ttf</summary>
<div>
<details>
    <summary>🔥 <b>FAIL</b> Check license file has good copyright string. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.license.html#"></a></summary>
    <div>







* 🔥 **FAIL** <p>First line in license file is:</p>
<p>&quot;copyright 20** the my font project authors (<a href="https://github.com/googlefonts/googlefonts-project-template">https://github.com/googlefonts/googlefonts-project-template</a>)&quot;</p>
<p>which does not match the expected format, similar to:</p>
<p>&quot;Copyright 2022 The Familyname Project Authors (git url)&quot;</p>
 [code: bad-format]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check math signs have the same width. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The most common width is 527 among a set of 2 math glyphs.
The following math glyphs have a different width, though:</p>
<p>Width = 622:
plus</p>
<p>Width = 481:
less</p>
<p>Width = 574:
equal</p>
<p>Width = 480:
greater</p>
<p>Width = 585:
logicalnot</p>
<p>Width = 553:
plusminus</p>
<p>Width = 537:
multiply</p>
<p>Width = 561:
divide</p>
<p>Width = 652:
minus</p>
<p>Width = 563:
approxequal</p>
<p>Width = 540:
notequal</p>
 [code: width-outliers]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Does the font contain a soft hyphen? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>This font has a 'Soft Hyphen' character.</p>
 [code: softhyphen]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/outline.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have on-curve points which have potentially incorrect y coordinates:</p>
<pre><code>* J (U+004A): X=140.5,Y=2.0 (should be at baseline 0?)

* uni004A0301 (U+E001): X=140.5,Y=2.0 (should be at baseline 0?)

* Jcircumflex (U+0134): X=140.5,Y=2.0 (should be at baseline 0?)

* uni01CE (U+01CE): X=228.0,Y=699.0 (should be at cap-height 700?)

* aogonek (U+0105): X=326.0,Y=2.0 (should be at baseline 0?)

* ccaron (U+010D): X=232.0,Y=699.0 (should be at cap-height 700?)

* ecaron (U+011B): X=246.0,Y=699.0 (should be at cap-height 700?)

* eogonek (U+0119): X=164.0,Y=-2.0 (should be at baseline 0?)

* m (U+006D): X=266.5,Y=522.0 (should be at x-height 520?)

* ncaron (U+0148): X=254.0,Y=699.0 (should be at cap-height 700?)

* oslash (U+00F8): X=15.0,Y=1.0 (should be at baseline 0?)

* oslashacute (U+01FF): X=15.0,Y=1.0 (should be at baseline 0?)

* rcaron (U+0159): X=155.0,Y=699.0 (should be at cap-height 700?)

* scaron (U+0161): X=200.0,Y=699.0 (should be at cap-height 700?)

* uogonek (U+0173): X=436.0,Y=-2.0 (should be at baseline 0?)

* zcaron (U+017E): X=200.0,Y=699.0 (should be at cap-height 700?)

* uni0417 (U+0417): X=258.5,Y=698.5 (should be at cap-height 700?)

* uni041B (U+041B): X=-31.0,Y=1.0 (should be at baseline 0?)

* uni0409 (U+0409): X=-31.0,Y=1.0 (should be at baseline 0?)

* uni0409 (U+0409): X=-31.0,Y=1.0 (should be at baseline 0?)

* uni0408 (U+0408): X=140.5,Y=2.0 (should be at baseline 0?)

* uni0474 (U+0474): X=724.5,Y=701.5 (should be at cap-height 700?)

* uni0498 (U+0498): X=258.5,Y=698.5 (should be at cap-height 700?)

* uni04DE (U+04DE): X=258.5,Y=698.5 (should be at cap-height 700?)

* uni0431 (U+0431): X=552.0,Y=702.0 (should be at cap-height 700?)

* uni0434 (U+0434): X=282.5,Y=698.5 (should be at cap-height 700?)

* uni0459 (U+0459): X=-7.0,Y=1.0 (should be at baseline 0?)

* uniFB4B (U+FB4B): X=243.5,Y=699.0 (should be at cap-height 700?)

* uni05E2 (U+05E2): X=13.0,Y=1.0 (should be at baseline 0?)

* uniFB2A (U+FB2A): X=718.5,Y=699.0 (should be at cap-height 700?)

* uniFB2B (U+FB2B): X=241.5,Y=699.0 (should be at cap-height 700?)

* uniFB2C (U+FB2C): X=718.5,Y=699.0 (should be at cap-height 700?)

* uniFB2D (U+FB2D): X=241.5,Y=699.0 (should be at cap-height 700?)

* uni05EA (U+05EA): X=31.0,Y=2.0 (should be at baseline 0?)

* uniFB4A (U+FB4A): X=31.0,Y=2.0 (should be at baseline 0?)

* one (U+0031): X=342.0,Y=699.0 (should be at cap-height 700?)

* one.tf (U+E009): X=398.0,Y=699.0 (should be at cap-height 700?)

* eight.tf (U+E010): X=487.0,Y=698.5 (should be at cap-height 700?)

* five.dnom (U+E018): X=61.5,Y=1.5 (should be at baseline 0?)

* uni2085 (U+2085): X=80.0,Y=-1.5 (should be at baseline 0?)

* questiondown (U+00BF): X=197.0,Y=-2.0 (should be at baseline 0?)

* parenleft (U+0028): X=288.0,Y=698.5 (should be at cap-height 700?)

* parenright (U+0029): X=199.0,Y=698.0 (should be at cap-height 700?)

* braceright (U+007D): X=296.5,Y=699.5 (should be at cap-height 700?)

* quotedblright (U+201D): X=252.0,Y=701.5 (should be at cap-height 700?)

* quotedblright (U+201D): X=386.0,Y=701.5 (should be at cap-height 700?)

* quoteright (U+2019): X=252.0,Y=701.5 (should be at cap-height 700?)

* at (U+0040): X=645.0,Y=-1.5 (should be at baseline 0?)

* lozenge (U+25CA): X=312.5,Y=701.5 (should be at cap-height 700?)

* lozenge (U+25CA): X=387.5,Y=699.5 (should be at cap-height 700?)

* uni030C (U+030C): X=35.0,Y=699.0 (should be at cap-height 700?)

* caron (U+02C7): X=35.0,Y=699.0 (should be at cap-height 700?)
</code></pre>
 [code: found-misalignments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check the direction of the outermost contour in each glyph <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/outline.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have a counter-clockwise outer contour:</p>
<pre><code>* uni05B8 (U+05B8) has a counter-clockwise outer contour
</code></pre>
 [code: ccw-outer-contour]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Ensure dotted circle glyph is present and can attach marks. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/shaping.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>No dotted circle glyph present</p>
 [code: missing-dotted-circle]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that replace the dot. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/shaping.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The dot of soft dotted characters used in orthographies <em>must</em> disappear in the following strings: į̀ į́ į̂ į̃ į̄ į̌ і́</p>
<p>The dot of soft dotted characters <em>should</em> disappear in other cases, for example: i̦̒ j̦̒ į̆ į̇ į̈ į̊ į̋ į̒ į̦̒ į̧̒ į̨̒ į̵̀ į̵́ į̵̂ į̵̃ į̵̄ į̵̆ į̵̇ į̵̈ į̵̊</p>
<p>Your font fully covers the following languages that require the soft-dotted feature: Ukrainian (Cyrl, 29,273,587 speakers), Lithuanian (Latn, 2,357,094 speakers), Belarusian (Cyrl, 10,064,517 speakers), Dutch (Latn, 31,709,104 speakers).</p>
<p>Your font does <em>not</em> cover the following languages that require the soft-dotted feature: Zapotec (Latn, 490,000 speakers), Southern Kisi (Latn, 360,000 speakers), Ngbaka (Latn, 1,020,000 speakers), Makaa (Latn, 221,000 speakers), Nzakara (Latn, 50,000 speakers), Navajo (Latn, 166,319 speakers), Koonzime (Latn, 40,000 speakers), Avokaya (Latn, 100,000 speakers), Dii (Latn, 71,000 speakers), Ejagham (Latn, 120,000 speakers), Mango (Latn, 77,000 speakers), Nateni (Latn, 100,000 speakers), Mfumte (Latn, 79,000 speakers), Fur (Latn, 1,230,163 speakers), Cicipu (Latn, 44,000 speakers), Gulay (Latn, 250,478 speakers), Ijo, Southeast (Latn, 2,471,000 speakers), Kom (Latn, 360,685 speakers), Igbo (Latn, 27,823,640 speakers), Sar (Latn, 500,000 speakers), Basaa (Latn, 332,940 speakers), Ma’di (Latn, 584,000 speakers), South Central Banda (Latn, 244,000 speakers), Bafut (Latn, 158,146 speakers), Lugbara (Latn, 2,200,000 speakers), Yala (Latn, 200,000 speakers), Dan (Latn, 1,099,244 speakers), Vute (Latn, 21,000 speakers), Kpelle, Guinea (Latn, 622,000 speakers), Bete-Bendi (Latn, 100,000 speakers), Ebira (Latn, 2,200,000 speakers), Ekpeye (Latn, 226,000 speakers), Mundani (Latn, 34,000 speakers), Aghem (Latn, 38,843 speakers).</p>
 [code: soft-dotted]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.subsets.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>The following codepoints supported by the font are not covered by
any subsets defined in the font's metadata file, and will never
be served. You can solve this by either manually adding additional
subset declarations to METADATA.pb, or by editing the glyphset
definitions.</p>
<ul>
<li>U+02C7 CARON: try adding one of: yi, canadian-aboriginal, tifinagh</li>
<li>U+02D8 BREVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02DB OGONEK: try adding one of: canadian-aboriginal, yi</li>
<li>U+02DD DOUBLE ACUTE ACCENT: not included in any glyphset definition</li>
<li>U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: coptic, cherokee, tifinagh, math</li>
<li>U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh</li>
<li>U+0307 COMBINING DOT ABOVE: try adding one of: math, canadian-aboriginal, old-permic, tai-le, tifinagh, coptic, syriac, malayalam</li>
<li>U+030A COMBINING RING ABOVE: try adding syriac</li>
<li>U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee</li>
<li>U+030C COMBINING CARON: try adding one of: cherokee, tai-le</li>
<li>U+0312 COMBINING TURNED COMMA ABOVE: not included in any glyphset definition</li>
<li>U+0326 COMBINING COMMA BELOW: not included in any glyphset definition</li>
<li>U+0327 COMBINING CEDILLA: not included in any glyphset definition</li>
<li>U+0328 COMBINING OGONEK: not included in any glyphset definition</li>
<li>U+0335 COMBINING SHORT STROKE OVERLAY: not included in any glyphset definition</li>
<li>U+0337 COMBINING SHORT SOLIDUS OVERLAY: not included in any glyphset definition</li>
<li>U+0338 COMBINING LONG SOLIDUS OVERLAY: not included in any glyphset definition</li>
<li>U+2021 DOUBLE DAGGER: try adding adlam</li>
<li>U+2030 PER MILLE SIGN: try adding adlam</li>
<li>U+2070 SUPERSCRIPT ZERO: not included in any glyphset definition</li>
<li>U+2075 SUPERSCRIPT FIVE: not included in any glyphset definition</li>
<li>U+2076 SUPERSCRIPT SIX: not included in any glyphset definition</li>
<li>U+2077 SUPERSCRIPT SEVEN: not included in any glyphset definition</li>
<li>U+2078 SUPERSCRIPT EIGHT: not included in any glyphset definition</li>
<li>U+2079 SUPERSCRIPT NINE: not included in any glyphset definition</li>
<li>U+207D SUPERSCRIPT LEFT PARENTHESIS: not included in any glyphset definition</li>
<li>U+207E SUPERSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition</li>
<li>U+2080 SUBSCRIPT ZERO: not included in any glyphset definition</li>
<li>U+2081 SUBSCRIPT ONE: not included in any glyphset definition</li>
<li>U+2082 SUBSCRIPT TWO: not included in any glyphset definition</li>
<li>U+2083 SUBSCRIPT THREE: not included in any glyphset definition</li>
<li>U+2084 SUBSCRIPT FOUR: not included in any glyphset definition</li>
<li>U+2085 SUBSCRIPT FIVE: not included in any glyphset definition</li>
<li>U+2086 SUBSCRIPT SIX: not included in any glyphset definition</li>
<li>U+2087 SUBSCRIPT SEVEN: not included in any glyphset definition</li>
<li>U+2088 SUBSCRIPT EIGHT: not included in any glyphset definition</li>
<li>U+2089 SUBSCRIPT NINE: not included in any glyphset definition</li>
<li>U+208D SUBSCRIPT LEFT PARENTHESIS: not included in any glyphset definition</li>
<li>U+208E SUBSCRIPT RIGHT PARENTHESIS: not included in any glyphset definition</li>
<li>U+212E ESTIMATED SYMBOL: not included in any glyphset definition</li>
<li>U+2153 VULGAR FRACTION ONE THIRD: not included in any glyphset definition</li>
<li>U+2154 VULGAR FRACTION TWO THIRDS: not included in any glyphset definition</li>
<li>U+215B VULGAR FRACTION ONE EIGHTH: not included in any glyphset definition</li>
<li>U+215C VULGAR FRACTION THREE EIGHTHS: not included in any glyphset definition</li>
<li>U+215D VULGAR FRACTION FIVE EIGHTHS: not included in any glyphset definition</li>
<li>U+215E VULGAR FRACTION SEVEN EIGHTHS: not included in any glyphset definition</li>
<li>U+2202 PARTIAL DIFFERENTIAL: try adding math</li>
<li>U+2206 INCREMENT: try adding math</li>
<li>U+220F N-ARY PRODUCT: try adding math</li>
<li>U+2211 N-ARY SUMMATION: try adding math</li>
<li>U+221A SQUARE ROOT: try adding math</li>
<li>U+221E INFINITY: try adding math</li>
<li>U+222B INTEGRAL: try adding math</li>
<li>U+2248 ALMOST EQUAL TO: try adding math</li>
<li>U+2260 NOT EQUAL TO: try adding math</li>
<li>U+2264 LESS-THAN OR EQUAL TO: try adding math</li>
<li>U+2265 GREATER-THAN OR EQUAL TO: try adding math</li>
<li>U+25CA LOZENGE: try adding one of: math, symbols</li>
<li>U+FB01 LATIN SMALL LIGATURE FI: not included in any glyphset definition</li>
<li>U+FB02 LATIN SMALL LIGATURE FL: not included in any glyphset definition</li>
</ul>
<p>Or you can add the above codepoints to one of the subsets supported by the font: <code>cyrillic</code>, <code>cyrillic-ext</code>, <code>greek-ext</code>, <code>hebrew</code>, <code>latin</code>, <code>latin-ext</code></p>
 [code: unreachable-subsetting]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Is there kerning info for non-ligated sequences? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.gpos.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>GPOS table lacks kerning info for the following non-ligated sequences:</p>
<pre><code>- f + f

- f + i

- f + l
</code></pre>
 [code: lacks-kern-info]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Ensure fonts have ScriptLangTags declared on the 'meta' table. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.meta.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>This font file does not have a 'meta' table.</p>
 [code: lacks-meta-table]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Checking OS/2 achVendID. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.os2.html#"></a></summary>
    <div>







* ⚠️ **WARN** <p>OS/2 VendorID value 'NONE' is not yet recognized. If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at <a href="https://www.microsoft.com/typography/links/vendorlist.aspx">https://www.microsoft.com/typography/links/vendorlist.aspx</a></p>
 [code: unknown]



</div>
</details>
</div>
</details>




### Summary

| 💥 ERROR | ☠ FATAL | 🔥 FAIL | ⚠️ WARN | ⏩ SKIP | ℹ️ INFO | ✅ PASS | 🔎 DEBUG | 
| ---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | 23 | 183 | 15 | 259 | 0 | 
| 0% | 0% | 0% | 5% | 38% | 3% | 54% | 0% | 



**Note:** The following loglevels were omitted in this report:


* SKIP
* INFO
* PASS
* DEBUG
