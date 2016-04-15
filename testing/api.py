from handlers import WordGraphValidatorHandler, GraphValidatorHandler
from .helpers import *
from unittest.mock import MagicMock


class TestWordGraphValidator(unittest.TestCase):

    def setUp(self):
        self.word_handler = WordGraphValidatorHandler()
        self.word_handler.json_data = {"nodes" : [{"id" : 1,
                                                   "ieml_string" : "[a.i.-]"},
                                                  {"id" : 2,
                                                   "ieml_string" : "[i.i.-]"},
                                                  {"id" : 3,
                                                   "ieml_string" : "[E:A:T:.]"},
                                                  {"id" : 4,
                                                   "ieml_string" : "[E:S:.wa.-]"},
                                                  {"id" : 5,
                                                   "ieml_string" : "[E:S:.o.-]"}
                                                  ],
                                       "graph": {"substance" : [1,2],
                                                 "mode" : [3,4,5]
                                                 },
                                       "tags" : {
                                           "fr" : "Faire du bruit avec sa bouche",
                                           "en" : "Blah blah blah"
                                       }
                                       }
        self.word_handler.db_connector = Mock()
        self.word_handler.do_request_parsing = MagicMock(name="do_request_parsing")

    def test_word_validation(self):
        """Tests the whole word validation code block without the request handling"""

        request_output = self.word_handler.post()
        word = get_test_word_instance()
        word.check()
        self.assertEquals(request_output["ieml"], str(word))

class TestSentenceGraphValidator(unittest.TestCase):

    def setUp(self):
        self.sentence_handler = GraphValidatorHandler()
        a, b, c, d, e, f = tuple(get_words_list())
        self.sentence_handler.json_data = {"validation_type" : 1,
                                           "nodes" : [{"id" : 1,
                                                       "ieml_string" : str(a)},
                                                      {"id" : 2,
                                                       "ieml_string" : str(b)},
                                                      {"id" : 3,
                                                       "ieml_string" : str(c)},
                                                      {"id" : 4,
                                                       "ieml_string" : str(d)},
                                                      {"id" : 5,
                                                       "ieml_string" : str(e)},
                                                      {"id" : 6,
                                                       "ieml_string" : str(f)}
                                                      ],
                                           "graph": [
                                               {"substance" : 1,
                                                "attribute" : 2,
                                                "mode" : 6},
                                               {"substance" : 1,
                                                "attribute" : 3,
                                                "mode" : 6},
                                               {"substance" : 2,
                                                "attribute" : 4,
                                                "mode" : 6},
                                               {"substance" : 2,
                                                "attribute" : 5,
                                                "mode" : 6}
                                           ],
                                           "tags" : {
                                               "fr" : "Danser sans les mains",
                                               "en" : "Do the poirier with the hands"
                                           }
                                           }
        self.sentence_handler.db_connector = Mock()
        self.sentence_handler.do_request_parsing = MagicMock(name="do_request_parsing")

    def test_sentence_validation(self):
        request_output = self.sentence_handler.post()
        sentence = get_test_sentence()
        sentence.order()
        self.assertEquals(request_output["ieml"], str(sentence))