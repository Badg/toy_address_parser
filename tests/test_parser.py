'''Contains tests for the parser.
'''
import pytest

from toy_address_parser.parser import parse

# Quick and dirty test cases. In a more realistic environment, it might be
# worthwhile to move these into a dedicated test vectors file. I'm putting them
# here for simplicity and time reasons, because packaging data files in python
# can sometimes be nontrivial
TEST_VECTORS_GERMAN = {
    'Winterallee 3': dict(street='Winterallee', housenumber='3'),
    'Musterstrasse 45': dict(street='Musterstrasse', housenumber='45'),
    'Musterstraße 45': dict(street='Musterstraße', housenumber='45'),
    'Blaufeldweg 123B': dict(street='Blaufeldweg', housenumber='123B'),
    'Am Bächle 23': dict(street='Am Bächle', housenumber='23'),
    'Auf der Vogelwiese 23 b':
        dict(street='Auf der Vogelwiese', housenumber='23 b'),
    'Irreweg 17 1/2': dict(street='Irreweg', housenumber='17 1/2'),
    'Irreweg 19.5': dict(street='Irreweg', housenumber='19.5'),
    'Postfach 10 01 65': dict(street='Postfach', housenumber='10 01 65'),
    'Ruhrstraße 32–34': dict(street='Ruhrstraße', housenumber='32–34'),
    'D1, 1-3': dict(street='D1', housenumber='1-3'),
}


@pytest.mark.parametrize('address,parsed', TEST_VECTORS_GERMAN.items())
def test_german_addresses(address, parsed):
    assert parse(address) == parsed
