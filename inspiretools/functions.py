"""Functions for extracting references."""

import re
import os
import logging
import argparse
import requests

LOGGER = logging.getLogger("inspiretools")

# blacklisted citation keys
BLACKLISTED_KEYS = [
    # from using revtex-4.1
    "REVTEX41Control",
    "apsrev41Control",
]


def aux2texkey(filename):
    """Extraxt TeX keys from an .aux file."""
    keys = []
    if not os.path.exists(filename):
        LOGGER.error("File %s not found.", filename)
        return keys
    with open(filename, "r") as f:
        lines = f.readlines()
    # regexp to match \citation{...} (bibtex) or abx@aux@cite{...} (biber)
    pattern = re.compile(r"^\\(citation|abx@aux@cite)\{(?P<keys>[^\}]+)\}$")
    # get nested list of texkeys
    keys = [
        re.search(pattern, c).group("keys").split(",")
        for c in lines
        if re.match(pattern, c)
    ]
    # flatten nested list
    keys = [item for sublist in keys for item in sublist]
    # remove duplicates
    keys = list(set(keys))
    # remove blacklisted keys
    keys = [x for x in keys if x not in BLACKLISTED_KEYS]
    return keys


def blg2texkey(filename):
    """Extract TeX keys from a .blg file."""
    keys = []
    if not os.path.exists(filename):
        LOGGER.error("File %s not found.", filename)
        return keys
    with open(filename, "r") as f:
        lines = f.readlines()
    # regexp to match 'Warning--I didn\'t find a database entry for "..."' (bibtex)
    # or 'WARN - I didn\'t find a database entry for '...'' (biber)
    pattern = re.compile(
        r".*I didn\'t find a database entry for [\"\'](?P<keys>[^\"]+)[\"\'].*"
    )
    # get nested list of texkeys
    keys = [
        re.search(pattern, c).group("keys").split(",")
        for c in lines
        if re.match(pattern, c)
    ]
    # flatten nested list
    keys = [item for sublist in keys for item in sublist]
    # remove duplicates
    keys = list(set(keys))
    # remove blacklisted keys
    keys = [x for x in keys if x not in BLACKLISTED_KEYS]
    return keys


def onerr(err, texkey):
    err += texkey + "\n"
    LOGGER.error("There was an error in trying" " to look up reference %s.", texkey)
    return err


def onnotfound(notfound, texkey):
    notfound += texkey + "\n"
    LOGGER.info("Reference %s not found on INSPIRE!", texkey)
    return notfound


def texkey2bib(texkeys):
    """Fetch BibTeX entry given TeX keys."""
    tot = len(texkeys)
    err = []
    notfound = []
    for i, texkey in enumerate(texkeys):
        try:
            LOGGER.info("Looking up reference %s of %s", str(i + 1), str(tot))
            inspire_query_params = {"q": "texkey=" + texkey, "format": "bibtex"}
            inspire_endpoint = "https://inspirehep.net/api/literature"
            res = requests.get(inspire_endpoint, params=inspire_query_params)
            res.raise_for_status()
            bib = res.text
            if bib != "":
                print(bib)
                LOGGER.info("Success.")
            else:
                notfound.append(texkey)
                LOGGER.warning("Reference %s not found on INSPIRE!", texkey)
        except KeyboardInterrupt:
            LOGGER.error("The reference extraction has been aborted before completion.")
            break
        except:
            err.append(texkey)
            LOGGER.error(
                "There was an error in trying to look up reference %s.", texkey
            )
    if err:
        LOGGER.error(
            "The following references could not be extracted due to errors:\n%s",
            "\n".join(err),
        )
    if notfound:
        LOGGER.error(
            "The following references could not be found on INSPIRE:\n%s",
            "\n".join(notfound),
        )


def aux2bib():
    """Generate bibliography from .aux file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="LaTeX .aux file", type=str)
    args = parser.parse_args()
    texkeys = aux2texkey(args.file)
    texkey2bib(texkeys)


def blg2bib():
    """Generate bibliography from .blg file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="BibTeX .blg file", type=str)
    args = parser.parse_args()
    texkeys = blg2texkey(args.file)
    texkey2bib(texkeys)
