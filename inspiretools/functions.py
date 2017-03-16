import re
import os
from . import pyinspire
import logging
from lxml import etree as et
import argparse

log = logging.getLogger('inspiretools')
log.setLevel(logging.INFO)

# blacklister citation keys
blacklisted_keys = [
    # from using revtex-4.1
    'REVTEX41Control', 'apsrev41Control'
]

def aux2texkey(filename):
    keys=[]
    if not os.path.exists(filename):
        log.error("File " + filename + " not found.")
        return keys
    with open(filename,'r') as f:
        lines = f.readlines()
    # regexp to match \citation{...} (bibtex) or abx@aux@cite{...} (biber)
    pattern = re.compile(r'^\\(citation|abx@aux@cite)\{(?P<keys>[^\}]+)\}$')
    # get nested list of texkeys
    keys = [re.search(pattern, c).group('keys').split(',')
            for c in lines if re.match(pattern, c)]
    # flatten nested list
    keys = [item for sublist in keys for item in sublist]
    # remove duplicates
    keys = list(set(keys))
    # remove blacklisted keys
    keys = [x for x in keys if x not in blacklisted_keys]
    return keys

def blg2texkey(filename):
    keys=[]
    if not os.path.exists(filename):
        log.error("File " + filename + " not found.")
        return keys
    with open(filename,'r') as f:
        lines = f.readlines()
    # regexp to match 'Warning--I didn\'t find a database entry for "..."' (bibtex)
    # or 'WARN - I didn\'t find a database entry for '...'' (biber)
    pattern = re.compile(r'.*I didn\'t find a database entry for [\"\'](?P<keys>[^\"]+)[\"\'].*')
    # get nested list of texkeys
    keys = [re.search(pattern, c).group('keys').split(',')
            for c in lines if re.match(pattern, c)]
    # flatten nested list
    keys = [item for sublist in keys for item in sublist]
    # remove duplicates
    keys = list(set(keys))
    # remove blacklisted keys
    keys = [x for x in keys if x not in blacklisted_keys]
    return keys

def onabort():
    print('The reference extraction has been aborted before completion.')

def onerr(err, texkey):
    err += texkey + '\n'
    log.error('There was an error in trying'
                  ' to look up reference ' + texkey +  '.')
    return err

def onnotfound(notfound, texkey):
    notfound  += texkey + '\n'
    log.info('Reference ' + texkey + ' not found on INSPIRE!')
    return notfound

def atend(err, notfound, before='', after=''):
    if err =='' and notfound=='':
        return
    print(before)
    if err != '':
        print('The following references could not be extracted due to errors:\n')
        print(err)
    if notfound != '':
        print('The following references could not be found on INSPIRE:\n')
        print(notfound)
    print(after)


def texkey2bib(texkeys):
    tot = len(texkeys)
    err=''
    notfound=''
    for i, texkey in enumerate(texkeys):
        try:
            log.info('Looking up reference ' + str(i+1)
                         + ' of ' + str(tot))
            bib = pyinspire.get_text_from_inspire('texkey ' + texkey, 'bibtex')
            if bib != '':
                print(bib)
                log.info('Success.')
            else:
                notfound = onnotfound(notfound, texkey)
        except KeyboardInterrupt:
            onabort()
            break
        except:
            err = onerr(err, texkey)
    atend(err, notfound)


def texkey2xml(texkeys, tags=245):
    tot = len(texkeys)
    err=''
    notfound=''
    first = True
    for i, texkey in enumerate(texkeys):
        try:
            log.info('Looking up reference ' + str(i+1)
                         + ' of ' + str(tot))
            bib = pyinspire.get_text_from_inspire('texkey ' + texkey, 'marcxml',
                                                  ot=tags)
            data = et.fromstring(bib.encode("utf-8"))
            if data.find('{http://www.loc.gov/MARC21/slim}record') is not None:
                if first:
                    xml = data
                    first = False
                else:
                    xml.extend(data)
                log.info('Success.')

            else:
                notfound = onnotfound(notfound, texkey)
        except KeyboardInterrupt:
            onabort()
            break
        except:
            err = onerr(err, texkey)

    if not first:
        print(et.tostring(xml, pretty_print=True).decode("utf-8"))

    atend(err, notfound, '<!--\n','-->')


def aux2bib():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="LaTeX .aux file",type=str)
    args = parser.parse_args()
    texkeys = aux2texkey(args.file)
    texkey2bib(texkeys)


def aux2xml():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="LaTeX .aux file",type=str)
    args = parser.parse_args()
    texkeys = aux2texkey(args.file)
    texkey2xml(texkeys)


def blg2bib():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="BibTeX .blg file", type=str)
    args = parser.parse_args()
    texkeys = blg2texkey(args.file)
    texkey2bib(texkeys)
