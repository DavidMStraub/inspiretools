import unittest
import os
from .functions import *

class TestParseaux(unittest.TestCase):
    def test_parseaux(self):
        """
        """
        this_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(this_dir, '..', 'examples', 'example.aux')
        keys = aux2texkey(filename)
        keys_correct = ["D'Agnolo:2012ie",'Straub:2013zca',
                        'Straub:2013uoa','Barbieri:2014tja',
                        'thisshouldntwork']
        self.assertCountEqual(keys,keys_correct)
