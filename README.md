# My Font

Description of your font goes here. We recommend to start with a very short presentation line (the kind you would use on twitter to present your project for example), and then add as much details as necesary :-) Origin of the project, idea of usage, concept of creation… but also number of masters, axes, character sets, etc.

Don't hesitate to create images!

![Sample Image](documentation/image1.png)

## About

Description of you and/or organisation goes here.

## Setting up your font

* Hit the green button above ("Use this template") to create your own repository.
    - *Make sure to click the checkbox marked "Include all branches".*

* Place your font sources in the `sources` directory.

 Unlike many open source distributors, Google Fonts is a **curated content**. Fonts shipped to the platform have to match the [Google Fonts Specifications](https://github.com/googlefonts/gf-docs/tree/main/Spec). Please read them carefully.

* Then reference the sources in the file `sources/config.yaml`, as well as making any other changes you would like to make based on the instructions in the [Google Font Builder documentation](https://github.com/googlefonts/gftools/blob/main/Lib/gftools/builder/__init__.py).


* Add yourself to the `AUTHORS.txt` and `CONTRIBUTORS.txt` files.

* Update the first line of the OFL.txt (year and project name). Update also the Copyright string in the sources, it has to be the same as the OFL.txt. The `.glyphs` file in this repo gives you required base charset and font info.

* Remove this section from the readme. :-)

* Finally, add and commit any files you have modified (i.e. `README.md`, `AUTHORS.txt`, `CONTRIBUTORS.txt`, the font sources, and `sources/config.yaml`) to git, then push to GitHub.

* Once you are happy with your font, add promotional assets in the documentation directory (format: 4:3). Make it different from the pic you use in this README.

## Building

Fonts are built automatically by GitHub Actions - take a look in the "Actions" tab for the latest build.

If you want to build fonts manually on your own computer:

* `make build` will produce font files.
* `make test` will run [FontBakery](https://github.com/googlefonts/fontbakery)'s quality assurance tests.
* `make proof` will generate HTML proof files.

The proof files and QA tests are also available automatically via GitHub Actions - look at `https://yourname.github.io/your-font-repository-name`.

## License

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at
https://scripts.sil.org/OFL

## Repository Layout

This font repository structure is inspired by [Unified Font Repository v0.3](https://github.com/unified-font-repository/Unified-Font-Repository), modified for the Google Fonts workflow.
