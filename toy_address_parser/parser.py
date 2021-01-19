'''Contains the actual address parsing logic.
'''
import dataclasses

from lark import Lark
from lark.visitors import Transformer


ADDRESS_GRAMMAR = r'''
    address: with_number_first | with_street_first
        | with_numbered_street_first | with_numbered_street_second

    // Note that these doesn't currently support eg "Apt 123" on the same line
    with_street_first: named_street ADDRESS_SEPARATOR? WS_INLINE housenumber
    with_number_first: housenumber ADDRESS_SEPARATOR? WS_INLINE named_street
    // Only common in the US (where it's extremely common)
    with_numbered_street_second:
        | housenumber ADDRESS_SEPARATOR? WS_INLINE numbered_street
    with_numbered_street_first:
        | numbered_street ADDRESS_SEPARATOR? WS_INLINE housenumber

    // We're assuming all housenumbers start with a number or a hard-coded
    // prefix, but can accommodate all sorts of weirdness thereafter. The .1/.2
    // indicate priority; in other words, streets take precedence over numbers
    housenumber: housenumber_prefix? housenumber_word+ housenumber_modifier?
    named_street.2: street_word (WS_INLINE street_word)*
    numbered_street.2: DIGIT+ ORDINAL WS_INLINE STREET_LITERAL
        | STREET_LITERAL WS_INLINE? DIGIT+

    street_word.3: LETTER (LETTER | DIGIT)*
    housenumber_prefix: HOUSENUMBER_PREFIX_WORD WS_INLINE?
    housenumber_word: (NUMBER | HOUSENUMBER_SYMBOL) WS_INLINE?
    // Include a maximum of one letter at the end of the number
    housenumber_modifier: WS_INLINE? LETTER

    // This works with unicode, unlike the common.LETTER
    LETTER: /\p{L}/
    // Currently just in english, since most numbered street names are USA.
    // Note that the i makes these case insensitive
    ORDINAL: "st"i | "nd"i | "rd"i | "th"i
    // Note: these are only used for numbered streets
    STREET_LITERAL: "calle"i | "st"i | "street"i | "ave"i | "avenue"i
    HOUSENUMBER_PREFIX_WORD: "no"i
    HOUSENUMBER_SYMBOL: "." | "/" | "-" | "–" | "—"
    // Putting this as a terminal in case we need to add periods
    ADDRESS_SEPARATOR: ","

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


def _join_children(self, children):
    return ''.join(children)


class CondenseTree(Transformer):
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

    This condenses that into a dictionary:
        {'street': 'Musterstraße', 'housenumber': '123'}
    '''
    named_street = _make_condensed_node('street')
    numbered_street = _make_condensed_node('street')
    housenumber = _make_condensed_node('housenumber')
    with_street_first = _convert_condensed_nodes_to_flat_dict
    with_number_first = _convert_condensed_nodes_to_flat_dict
    with_numbered_street_first = _convert_condensed_nodes_to_flat_dict
    with_numbered_street_second = _convert_condensed_nodes_to_flat_dict
    street_word = _join_children
    housenumber_word = _join_children
    housenumber_prefix = _join_children
    housenumber_modifier = _join_children

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
    condensed_tree = CondenseTree().transform(parse_tree)
    return condensed_tree
