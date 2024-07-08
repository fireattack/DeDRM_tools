# DeDRM tools - Mini

This is a minimized version of [DeDRM tools](https://github.com/apprenticeharper/DeDRM_tools) which removes all the unnecessary files and folders, leaving only the files needed to run standalone DRM removal scripts for Kindle.

Also dramatically simplified the code by removing all kinds of messy code. E.g.:

* Removed all the Python 2 compatibility code.
* Change all the imports to relative imports.
* Support pycryptodome (Crypto) only.
* Support only the native lzma module.
* Remove all kinds of stdout/stderr hacks.
* TODO: remove all the CLI related code.
* TODO: remove all the GUI related code.

See https://github.com/noDRM/DeDRM_tools/compare/master...fireattack:DeDRM_tools:mini for a full list of changes.

It is meant to be used within [extract_kindle](https://github.com/fireattack/extract_kindle) project.