# INSPIRE tools

This Python 3 package provides two scripts, `auxtobib` and `auxtoxml`, which take a LaTeX `.aux` file as input. 
`auxtobib` fetches the `bibtex` entries for all the articles cited in the document from
[INSPIRE](http://inspirehep.net/). `auxtoxml` return an XML file containing the titles of the articles.

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
The script to generate an XML file works analogously,
```
auxtoxml paper.aux > bibliography.xml
```
