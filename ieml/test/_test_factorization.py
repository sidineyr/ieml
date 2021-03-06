from ieml.dictionary import Dictionary
from ieml.dictionary.script import factorize
import unittest

class FactorizationTest(unittest.TestCase):
    def test_all_terms(self):
        for t in Dictionary():
            f = factorize(t.script)
            self.assertEqual(t.script, f, "Invalid factorization for term %s -> %s"%(str(t), str(f)))

