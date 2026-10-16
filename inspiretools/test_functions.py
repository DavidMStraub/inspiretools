import unittest
import os
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

from .functions import aux2texkey, texkey2bib


class TestParseaux(unittest.TestCase):
    def test_parseaux(self):
        """"""
        this_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(this_dir, "..", "examples", "example.aux")
        keys = aux2texkey(filename)
        keys_correct = [
            "D'Agnolo:2012ie",
            "Straub:2013zca",
            "Straub:2013uoa",
            "Barbieri:2014tja",
            "thisshouldntwork",
        ]
        self.assertCountEqual(keys, keys_correct)


class TestTexkey2bib(unittest.TestCase):
    def test_uses_current_inspire_key_by_default(self):
        output = StringIO()
        response = Mock()
        response.text = "@article{LHCb:2014cxe,\n}"

        with patch("inspiretools.functions.requests.get", return_value=response), redirect_stdout(output):
            texkey2bib(["Aaij:2014pli"])

        self.assertIn("@article{LHCb:2014cxe,", output.getvalue())
        self.assertNotIn("@article{Aaij:2014pli,", output.getvalue())

    def test_keep_old_texkeys_preserves_original_key(self):
        output = StringIO()
        response = Mock()
        response.text = "@article{LHCb:2014cxe,\n}"

        with patch("inspiretools.functions.requests.get", return_value=response), redirect_stdout(output):
            texkey2bib(["Aaij:2014pli"], keep_old_texkeys=True)

        self.assertIn("@article{Aaij:2014pli,", output.getvalue())
