
![Build Status](https://github.com/github/vmalloc/emport/workflows/main.yml/badge.svg)
![Supported Versions](https://img.shields.io/pypi/pyversions/emport.svg)
![Latest Version](https://img.shields.io/pypi/v/emport.svg)


Overview
========

Emport is a small utility library for importing files by file name. It exposed a single function, ``import_file(filename)``.

Unlike traditional usages of ``__import__``, ``execfile`` or even ``imp.load_source``, Emport takes care of all cases that you may encounter - importing files inside packages (useful when they use relative imports), importing directories (or ``__init__.py`` files)


Licence
=======

The library is licensed under the BSD (3-clause) open source license.



