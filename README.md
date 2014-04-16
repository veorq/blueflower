blueflower
==========

blueflower looks for secrets such as private keys or passwords in a file
structure.
Interesting files are detected using heuristics on their names and on
their content.
blueflower prioritizes speed, hence there may be a lot of false
positives.

Unlike some forensics tools, blueflower does not search in RAM, and
does not attempt to identify cryptographic keys or algorithms in
binaries.  

**DISCLAIMER:** This program is under development. It may not work as
expected and it may destroy your computer. Use at your own risk.


Features
------------

* support of 
    - `text/*` MIME-typed files
    - ZIP archives
    - tar archives
* portable \*nix/Windows


### TODO

* support of
    - PDFs
    - DOC(X), XLS(X), PPT(X); Open/LibreOffice equivalents
    - compressed files
* detection of encrypted files

Usage
------------

```Python
make install
blueflowery [path]
```

Results are written to a file `blueflower-YYYYMMDDhhmmss`.

*WARNING*: no limit is set on the number of files processed.


Dependencies
------------

* [python-magic](https://github.com/ahupp/python-magic)


License
-------

blueflower is released under GPLv3. Copyright Jean-Philippe Aumasson 2014.
