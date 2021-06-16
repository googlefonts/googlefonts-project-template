# My Font

Short description of your font goes here.

## Setting up your font

* Hit the green button above ("Use this template") to create your own repository.
    - *Make sure to click the checkbox marked "Include all branches".*

* Place your font sources in the `sources` directory.

* Then reference the sources in the file `sources/config.yaml`, as well as making any other changes you would like to make based on the instructions in the [Google Font Builder documentation](https://github.com/googlefonts/gftools/blob/main/Lib/gftools/builder/__init__.py).

* Add yourself to the `AUTHORS.txt` and `CONTRIBUTORS.txt` files.

* Remove this section from the readme. :-)

* Finally, add and commit any files you have modified (i.e. `README.md`, `AUTHORS.txt`, `CONTRIBUTORS.txt`, the font sources, and `sources/config.yaml`) to git, then push to GitHub.

## Building

Fonts are built automatically by GitHub Actions - take a look in the "Actions" tab for the latest build.

If you particularly want to build fonts manually on your own computer, you will need to install the [`yq` utility](https://github.com/mikefarah/yq). On OS X with Homebrew, type `brew install yq`; on Linux, try `snap install yq`; if all else fails, try the instructions on the linked page.

Then:

* `make build` will produce font files.
* `make test` will run [FontBakery](https://github.com/googlefonts/fontbakery)'s quality assurance tests.
* `make proof` will generate HTML proof files.

The proof files and QA tests are also available automatically via GitHub Actions - look at `https://yourname.github.io/your-font-repository-name`.

## License

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at
http://scripts.sil.org/OFL

## Repository Layout

This font repository structure is inspired by [Unified Font Repository v0.3](https://github.com/unified-font-repository/Unified-Font-Repository), modified for the Google Fonts workflow.
