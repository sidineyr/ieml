from itertools import zip_longest

from ieml.exceptions import InvalidGraphNode
from ieml.ieml_objects.commons import IEMLObjects, TreeGraph
from ieml.ieml_objects.constants import MAX_NODES_IN_SENTENCE
from ieml.ieml_objects.exceptions import InvalidIEMLObjectArgument, InvalidTreeStructure
from ieml.ieml_objects.words import Word


class AbstractClause(IEMLObjects):
    def __init__(self, subtype, substance=None, attribute=None, mode=None, children=None):
        if not (substance or children):
            raise ValueError()

        if children is None:
            children = [substance, attribute, mode]
            if any(e is None for e in children):
                raise InvalidIEMLObjectArgument(self.__class__, "Must specify a substance, an attribute and a mode.")

        if len(children) != 3:
            raise InvalidIEMLObjectArgument(self.__class__, "A clause must have three children (%d provided)."%len(children))

        if not all(isinstance(e, subtype) for e in children):
            raise InvalidIEMLObjectArgument(self.__class__, "The children of a %s must be a %s instance."%
                                            (self.__class__.__name__, subtype.__name__))

        if children[0] == children[1]:
            raise InvalidIEMLObjectArgument(self.__class__, "The attribute and the substance (%s) must be distinct."%
                                            (str(children[0])))

        super().__init__(children)

    @property
    def substance(self):
        return self.children[0]

    @property
    def attribute(self):
        return self.children[1]

    @property
    def mode(self):
        return self.children[2]

    @property
    def grammatical_class(self):
        return self.attribute.grammatical_class

    def compute_str(self, children_str):
        return '('+'*'.join(children_str)+')'


class AbstractSentence(IEMLObjects):
    def __init__(self, subtype, clause_list, literals=None):
        try:
            _children = tuple(e for e in clause_list)
        except TypeError:
            raise InvalidIEMLObjectArgument(self.__class__, "The argument %s is not an iterable" % str(clause_list))

        if not all(isinstance(e, subtype) for e in _children):
            raise InvalidIEMLObjectArgument(self.__class__, "The children of a %s must be %s instance."%
                                            (self.__class__.__name__, subtype.__name__))

        try:
            self.tree_graph = TreeGraph(((c.substance, c.attribute, c) for c in _children))
        except InvalidTreeStructure as e:
            raise InvalidIEMLObjectArgument(self.__class__, e)

        if len(self.tree_graph.nodes) > MAX_NODES_IN_SENTENCE:
            raise InvalidIEMLObjectArgument(self.__class__, "Too many distinct nodes: %d>%d."%
                                            (len(self.tree_graph.nodes), MAX_NODES_IN_SENTENCE))

        super().__init__((e for stage in self.tree_graph.stages for e in sorted((t[1] for s in stage for t in self.tree_graph.transitions[s]))), literals=literals)

    @property
    def grammatical_class(self):
        return self.tree_graph.root.grammatical_class

    def compute_str(self, children_str):
        return '[' + '+'.join(children_str) + ']'


class Clause(AbstractClause):
    def __init__(self, substance=None, attribute=None, mode=None, children=None):
        super().__init__(Word, substance=substance, attribute=attribute, mode=mode, children=children)


class Sentence(AbstractSentence):
    def __init__(self, clause_list, literals=None):
        super().__init__(Clause, clause_list=clause_list, literals=literals)


class SuperClause(AbstractClause):
    def __init__(self, substance=None, attribute=None, mode=None, children=None):
        super().__init__(Sentence, substance=substance, attribute=attribute, mode=mode, children=children)


class SuperSentence(AbstractSentence):
    def __init__(self, clause_list, literals=None):
        super().__init__(SuperClause, clause_list=clause_list, literals=literals)
