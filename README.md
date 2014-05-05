blueflower
==========

![logo](blueflower.jpg)

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

* detection of various key and password containers (SSH, Apple keychain,
  Java KeyStore, etc.) and other interesting files (Bitcoin wallets, PGP
  policies, etc.)
* detection of encrypted containers (Truecrypt, PGP Disks, GnuPG files, etc.)
* search in the content of the following types of files:
    - `text/*` MIME-typed files
    - archives RAR, tar, ZIP
    - compressed files bzip2, gzip
    - encrypted containers/archives: PGP/GPG, Truecrypt, RAR, ZIP
    - PDF documents
* support of nested archives and compressed files (except for nested RARs)
* portable \*nix/Windows
* CSV output


### TODO

* \*Office documents
* more secrecy heuristics
* more type recognition heuristics
* speed optimizations


Usage
------------

Installation:
```
sudo make
```
(omit `sudo` on Windows)

Execution:
```
blueflower directory
```

Results are written to a file `blueflower-YYYYMMDDhhmmss`. Hit `^C` to
interrupt.

The `makefile` defines `make clean`, `make cleanall`, and `make dist`.

**WARNINGS:**

* no limit is set on the number of files processed
* there may be a lot of false positives


Dependencies
------------

Python modules:
* [pdfminer](https://pypi.python.org/pypi/pdfminer/)
* [python-magic](https://pypi.python.org/pypi/python-magic/)
* [rarfile](https://pypi.python.org/pypi/rarfile/)

Other:
* `unrar` utility


License
-------

blueflower is released under GPLv3. Copyright Jean-Philippe Aumasson 2014.
