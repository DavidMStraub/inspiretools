#!/usr/bin/env python
'''
pyinspire - command line retrieval of INSPIRE HEP database results
Author: Ian Huston
Released under the modified BSD license.

Example: pyinspire.py -b -s "find a Feynman, Richard"
'''
import sys
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from bs4 import BeautifulSoup
import optparse
import logging
import re

__version__ = "0.3.0"
APIURL = "http://old.inspirehep.net/search?"
logging.basicConfig()
log = logging.getLogger("pyinspire")


def get_text_from_inspire(search="", resultformat="brief", ot=None):
    """Extract text from an INSPIRE search."""
    log.info("Search of INSPIRE started...")
    data = query_inspire(search, resultformat=resultformat, ot=ot)
    if resultformat == "marcxml" or  resultformat == "json":
        text = data.decode("utf-8")
    else:
        text = extract_from_data(data)
    return text

def inspire_url(search="", resultformat="brief", startrecord=0, ot=None):
    """Construct the query string for INSPIRE"""
    formats = {"brief": "hb",
               "bibtex": "hx",
               "latexEU": "hlxe",
               "latexUS": "hlxu",
               "marcxml": "xm",
               "json": "recjson"}
    inspireoptions = dict(action_search="Search",
                          rg=100, #number of results to return in one page
                          of=formats[resultformat], # format of results
                          ln="en", #language
                          p=search, # search string
                          jrec=startrecord, # record number to start at
                          )
    if resultformat == "marcxml" or resultformat == "json":
        if ot is None and resultformat == "marcxml":
            ot = '100,700,245' # default: return authors & title only
        if ot is None and resultformat == "json":
            ot = 'authors,title' # default: return authors & title only
        inspireoptions['ot'] = ot

    url = APIURL + urlencode(inspireoptions)
    return url

def query_inspire(search="", resultformat="brief", ot=None):
    """Query the INSPIRE HEP database and return the entries.

    Parameters
    ----------
    search : string
             search string to use in query

    resultformat : string
             long hand name of format, ["brief", "bibtex", "latexEU", "latexUS"]

    """
    url = inspire_url(search, resultformat, ot=ot)
    log.debug("Query URL is %s", str(url))

    try:
        f = urlopen(url)
        log.debug("Starting to read data from %s.", str(url))
        data = f.read()
        log.debug("Data has been read: \n %s", str(data))
    except IOError as e:
        log.error("Error retrieving results: %s", str(e))
        raise
    return data

def extract_from_data(data):
    soup = BeautifulSoup(data, "lxml")

    if soup.pre:
        text = extract_pre_tags(soup)
    else:
        text = extract_text(soup)

    return text

def extract_pre_tags(soup):
    """Extract text from <pre> tags in BeautifulSoup soup."""
    text = "\n".join([tag.text for tag in soup.find_all("pre")])
    return text

def citecount(text):
    """Return the number of citations as specified by the
    string 'Cited by X records'"""
    match = re.search(r"Cited by (\d*) records", text)
    if match:
        cites = int(match.groups()[0])
    else:
        cites = 0
    return cites


def extract_text(soup):
    """Extract useful text from BeautifulSoup soup"""
    mainbodies = soup.find_all("div", {"class":"record_body"})
    moreinfos = soup.find_all("div", {"class":"moreinfo"})
    if len(mainbodies) != len(moreinfos):
        raise ValueError("Number of records is inconsistent.")
    if len(mainbodies) == 0:
        log.info("No useful information found in text.")
        return ""
    [t.small.ul.replaceWith("") for t in mainbodies if t.small.ul]
    moreinfotext = [mi.text.replace("Detailed record - ", "") for mi in moreinfos]
    ts = [mb.text + "\n" + mi for mb, mi in zip(mainbodies, moreinfotext) ]
    text = ("\n"+40*"="+"\n").join(ts).replace("\n\n", "\n")
    return text

def extract_details(soup):
    """Extract title, authors, arxivnum and citation count"""
    mainbodies = soup.find_all("div", {"class":"record_body"})
    moreinfos = soup.find_all("div", {"class":"moreinfo"})
    if len(mainbodies) != len(moreinfos):
        raise ValueError("Number of records is inconsistent.")
    if len(mainbodies) == 0:
        log.info("No useful information found in text.")
        return []
    details = []
    for mb, mi in zip(mainbodies, moreinfos):
        d = {"title": mb.findAll("a", {"class":"titlelink"})[0].text,
             "authors": [m.text for m in mb.findAll("a", {"class":"authorlink"})],
             "citations": citecount(mi.text)}
        details.append(d)
    return details

def main(argv=None):
    """ Main method to deal with command line arguments.

    """
    if not argv:
        argv = sys.argv
    #Parse command line options
    usage = "%prog [options] -s \"INSPIRE search string\"\n" + __doc__
    parser = optparse.OptionParser(usage=usage, version=__version__)

    parser.add_option("-s", "--search", action="store", dest="search",
                      type="string",
                      metavar="STRING", help="search string to send to INSPIRE")

    parser.add_option("-b", "--bibtex", action="store_const",
                      dest="resultformat", const="bibtex", default="brief",
                  help="output bibtex for entries")
    parser.add_option("--latexEU", action="store_const",
                      dest="resultformat", const="latexEU",
                  help="use LaTeX(EU) format for entries")
    parser.add_option("--latexUS", action="store_const",
                      dest="resultformat", const="latexUS",
                  help="use LaTeX(US) for entries")
    parser.add_option("-x", "--marcxml", action="store_const",
                      dest="resultformat", const="marcxml", default="brief",
                  help="output MarcXML for entries")
    parser.add_option("-j", "--json", action="store_const",
                      dest="resultformat", const="json", default="brief",
                  help="output JSON for entries")
    parser.add_option("-t", "--tags", action="store",
                      dest="tags", type="string",
                  help="specify tags to be included in MarcXML or JSON output")
    parser.add_option("-v", "--verbose",
                  action="store_const", const=logging.INFO, dest="loglevel",
                  help="print informative messages", default=logging.INFO)
    parser.add_option("--debug",
                  action="store_const", const=logging.DEBUG, dest="loglevel",
                  help="log lots of debugging information")

    (options, args) = parser.parse_args(args=argv[1:])

    log.setLevel(options.loglevel)
    log.debug("pyinspire called with the following options:\n %s", str(options))

    try:
        result = get_text_from_inspire(options.search, options.resultformat,
                                       options.tags)
        log.debug("Successfully extracted text from search.")
        print(result)
    except Exception as e:
        log.error("Error during retrieval of results: %s", str(e))
        return 1
    log.debug("Successfully exited.")
    return 0




if __name__ == "__main__":
    sys.exit(main(sys.argv))
