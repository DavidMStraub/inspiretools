import re
import os
import pyinspire
from lxml import etree as et

def aux2texkey(filename):
    keys=[]
    if not os.path.exists(filename):
        print("Error: file " + filename + " not found.")
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
    return keys

def onabort():
    print('The reference extraction has been aborted before completion.')

def atend(err, notfound):
    if err != '':
        print('The following references could not be extracted due to errors:\n')
        print(err)

    if notfound != '':
        print('The following references could not be found on INSPIRE:\n')
        print(notfound)


def texkey2bib(texkeys):
    err=''
    notfound=''
    for texkey in texkeys:
        try:
            bib = pyinspire.get_text_from_inspire('texkey ' + texkey, 'bibtex')
            if bib != '':
                print(bib)
            else:
                notfound  += texkey + '\n'
        except KeyboardInterrupt:
            onabort()
            break
        except:
            err += texkey + '\n'
    atend(err, notfound)


def texkey2xml(texkeys, tags=245):
    err=''
    notfound=''
    first = True
    for texkey in texkeys:
        try:
            bib = pyinspire.get_text_from_inspire('texkey ' + texkey, 'marcxml',
                                                  ot=tags)
            data = et.fromstring(bib.encode("utf-8"))
            if data.find('{http://www.loc.gov/MARC21/slim}record') is not None:
                if first:
                    xml = data
                    first = False
                else:
                    xml.extend(data)

            else:
                notfound  += texkey + '\n'
        except KeyboardInterrupt:
            onabort()
            break
        except:
            err += texkey + '\n'

    if not first:
        print(et.tostring(xml, pretty_print=True).decode("utf-8"))

    atend(err, notfound)
