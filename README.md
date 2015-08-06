# INSPIRE tools

At the moment, this Python 3 package provides a single tool, namely a script
`auxtobib` that takes a LaTeX `.aux` file as input and fetches the `bibtex`
entries for all the articles cited in the document from
[INSPIRE](http://inspirehep.net/)

## Installation


To install the package in your home directory, execute the following command in
the package's root directory,
```
pip3 install . --user
```

## Requirements

The script was tested with Python 3.4. It requires `pyinspire`.

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
