# INSPIRE tools

This Python 3 package provides two scripts, `auxtobib` and `blgtobib`, which take a LaTeX `.aux` or `.blg` file as input.
`auxtobib` fetches the `bibtex` entries for all the articles cited in the document from
[INSPIRE](http://inspirehep.net/). `blgtobib` does the same, but only fetches those entries which are missing.

## Installation


To install the package in your home directory, run
```
python3 -m pip install inspiretools --user
```

## Requirements

The script requires Python 3.5+.

## Usage

Given a LaTeX `.aux` file, simply execute
```
auxtobib paper.aux
```
and the `bibtex` entries will be printed to `stdout`. If you want to save them
into a `.bib` file, simply use
```
auxtobib paper.aux > bibliography.bib
```

The script `blgtobib` will fetch only `bibtex` entries which are not already in
the `.bib` file associated with your project. It uses the `bibtex` log file
associated with the LaTeX project. For example,
```
blgtobib paper.blg >> bibliography.bib
```
will append new entries to `bibliography.bib`.
