from multiprocessing.dummy import Pool as ThreadPool
import unittest
from ieml.dictionary.dictionary import Dictionary
from ieml.dictionary.script.operator import script

from ieml.exceptions import TermNotFoundInDictionary, CannotParse
from ieml.syntax.parser.parser import IEMLParser
from ieml.syntax import Text
from ieml.syntax.terms import SyntaxTerm
from ieml.tools import RandomPoolIEMLObjectGenerator, ieml
from ieml.dictionary import term


class TestPropositionParser(unittest.TestCase):

    def setUp(self):
        self.rand = RandomPoolIEMLObjectGenerator(level=Text)
        self.parser = IEMLParser()

    def test_parse_term(self):

        for i in range(10):
            o = self.rand.term()
            self.assertEqual(self.parser.parse(str(o)), o)

    def test_parse_word(self):
        for i in range(10):
            o = self.rand.word()
            self.assertEqual(self.parser.parse(str(o)), o)

    def test_parse_term_plus(self):
        t = term("f.-O:M:.+M:O:.-s.y.-'")
        to_check = ieml("[f.-O:M:.+M:O:.-s.y.-']")
        self.assertEqual(to_check, SyntaxTerm(t))

    def test_parse_sentence(self):
        for i in range(10):
            o = self.rand.sentence()
            self.assertEqual(self.parser.parse(str(o)), o)

    def test_parse_super_sentence(self):
        for i in range(10):
            o = self.rand.word()
            self.assertEqual(self.parser.parse(str(o)), o)

    def test_parse_text(self):
        for i in range(10):
            o = self.rand.text()
            self.assertEqual(self.parser.parse(str(o)), o)

    def test_literals(self):
        w1 = str(self.rand.word()) + "<la\la\>lal\>fd>"
        w2 = str(self.rand.word()) + "<@!#$#@%{}\>fd>"
        self.assertEqual(str(self.parser.parse(w1)), w1)
        self.assertEqual(str(self.parser.parse(w2)), w2)
        s1 = '[('+ '*'.join((w1, w2, str(self.rand.word()))) +')]' + "<!@#$%^&*()_+\<>"
        self.assertEqual(str(self.parser.parse(s1)), s1)
        ss1 = '[('+ '*'.join((s1, str(self.rand.sentence()), str(self.rand.sentence()))) + ')]<opopop>'
        self.assertEqual(str(self.parser.parse(ss1)), ss1)

    def test_invalid_term(self):
        with self.assertRaises(CannotParse):
            self.parser.parse("[([A:A:A:.-'])]")

        with self.assertRaises(TermNotFoundInDictionary):
            term("A:A:A:.")

    def test_multiple_ieml_parser(self):
        p0 = IEMLParser()
        p1 = IEMLParser()
        self.assertEqual(p0, p1)

        p2 = IEMLParser(Dictionary('dictionary_2017-06-07_00:00:00'))
        self.assertNotEqual(p0, p2)

        p3 = IEMLParser(from_version='dictionary_2017-06-07_00:00:00')
        self.assertNotEqual(p2, p3)

    def test_parse_script(self):
        self.assertEqual(str(self.parser.parse("A:")), '[A:]')

    def test_threading(self):
        pool = ThreadPool(4)
        results = pool.map(self.parser.parse, Dictionary().version.terms)
        self.assertSetEqual({str(t) for t in results}, {'[{0}]'.format(str(t)) for t in Dictionary().version.terms})

        results = pool.map(script, Dictionary().version.terms)
        self.assertSetEqual({str(t) for t in results}, set(Dictionary().version.terms))

