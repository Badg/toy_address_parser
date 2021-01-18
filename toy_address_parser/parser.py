'''Contains the actual address parsing logic.
'''
import dataclasses

from lark import Lark
from lark.visitors import Transformer


ADDRESS_GRAMMAR = r'''
    address: (german_address | french_address | usa_address)

    // Germany: street name, occasionally followed by a comma (eg districts
    // in der Innenstadt Mannheims), followed by housenumber
    german_address: named_street ADDRESS_SEPARATOR? WS_INLINE housenumber
    french_address: named_street ADDRESS_SEPARATOR? WS_INLINE housenumber
        | housenumber ADDRESS_SEPARATOR? WS_INLINE named_street
    // Note that this doesn't currently support eg "Apt 123" on the same line
    usa_address: housenumber WS_INLINE (named_street | numbered_street)

    // We're assuming all housenumbers start with a number, but can be flexible
    // from there, to accommodate all sorts of weirdness
    housenumber: NUMBER (WS_INLINE? (DIGIT | LETTER | HOUSENUMBER_SYMBOL)+)*
    named_street: street_word (WS_INLINE street_word)*
    numbered_street: DIGIT+ ORDINAL

    // Enforce that words in street names must start with letters, but may
    // contain numbers. This breaks on tons and tons of US streets, eg 14th St
    street_word: LETTER (LETTER | DIGIT)*

    LETTER: /\p{L}+/
    HOUSENUMBER_SYMBOL: ("." | "/" | "-" | "–" | "—")
    // Putting this as a terminal in case we need to add periods
    ADDRESS_SEPARATOR: ","
    // Currently just in english, since most numbered street names are USA
    ORDINAL: "st" | "sT" | "St" | "ST"
        | "nd" | "nD" | "Nd" | "ND"
        | "rd" | "rD" | "Rd" | "RD"
        | "th" | "tH" | "Th" | "TH"

    %import common.DIGIT
    %import common.NUMBER
    %import unicode.WS_INLINE
'''


def _make_condensed_node(node_type):
    '''This creates a function that produces a condensed node for the
    passed node_type. It's a little redundant naming-wise, since you
    need to type the node_type twice, but it's less confusing than a
    decorator would be. Believe me, I wrote the decorator and really
    didn't like it. Although one advantage to the redundancy is that we
    can collapse both named and numbered streets to simply be called
    "streets"!
    '''

    def condensate(self, children):
        return CondensedNode(
            node_type=node_type,
            node_value=''.join(children)
        )

    return condensate


def _convert_condensed_nodes_to_flat_dict(self, children):
    '''Use this for converting a tree of CondensedNode instances into a
    flat dictionary.
    '''
    return {
        child.node_type: child.node_value
        for child in children
        if isinstance(child, CondensedNode)
    }


class CondenseTokens(Transformer):
    '''A raw parse tree looks like this:
        address
            german_address
                street
                    street_word
                        W
                        i
                        n
                        t
                        e
                        r
                        a
                        l
                        l
                        e
                        e
                housenumber 3

    This condenses that into
        address
            german_address
                street Winterallee
                housenumber 3
    '''
    named_street = _make_condensed_node('street')
    numbered_street = _make_condensed_node('street')
    housenumber = _make_condensed_node('housenumber')
    german_address = _convert_condensed_nodes_to_flat_dict
    french_address = _convert_condensed_nodes_to_flat_dict
    usa_address = _convert_condensed_nodes_to_flat_dict

    def street_word(self, children):
        return ''.join(children)

    def address(self, children):
        return children[0]


@dataclasses.dataclass(frozen=True)
class CondensedNode:
    node_type: str
    node_value: str


# Use alternative regex for proper unicode support
_PARSER = Lark(
    ADDRESS_GRAMMAR,
    regex=True,
    start='address')


def parse(address: str):
    # Let parent handle parse errors
    parse_tree = _PARSER.parse(address)
    condensed_tree = CondenseTokens().transform(parse_tree)
    return condensed_tree
