import re
import os

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
