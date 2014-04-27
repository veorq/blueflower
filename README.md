blueflower
==========

blueflower is a simple tool that looks for secrets such as private keys
or passwords in a file structure.
Interesting files are detected using heuristics on their names and on
their content.

Unlike some forensics tools, blueflower does not search in RAM, and
does not attempt to identify cryptographic keys or algorithms in
binaries.

**DISCLAIMER:** This program is under development. It may not work as
expected and it may destroy your computer. Use at your own risk.


Features
------------

* support of the following types of files:
    - `text/*` MIME-typed files
    - bzip2 compressed files
    - gzip compressed files
    - RAR archives
    - tar archives
    - ZIP archives
* support of nested archives and compressed files (except for nested RARs)
* portable \*nix/Windows
* CSV output


### TODO

* support of PDFs, \*Office documents
* flagging of encrypted archives
* detection of encrypted files/containers
* speed optimizations


Usage
------------

Installation:
```
sudo make
```

Execution:
```
blueflower [directory]
```

Results are written to a file `blueflower-YYYYMMDDhhmmss`.

The `makefile` defines `make clean`, `make cleanall`, and `make dist`.

**WARNINGS:**

* no limit is set on the number of files processed
* there may be a lot of false positives


Dependencies
------------

Python modules:
* [python-magic](https://github.com/ahupp/python-magic)
* [rarfile](https://pypi.python.org/pypi/rarfile/2.6)

Other:
* `unrar` utility


License
-------

blueflower is released under GPLv3. Copyright Jean-Philippe Aumasson 2014.
