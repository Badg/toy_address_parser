'''Contains all exception subclasses used by toy_address_parser in a
single location with no internal dependencies. This makes it a lot
easier to avoid accidental circular imports in exception handling logic.
'''


class ToyAddressParserException(Exception):
    '''The base class for all of our internal exceptions. You can catch
    this to handle all expected errors from within toy_address_parser;
    anything that would leak through that catch would be a
    toy_address_parser bug. This idiom is more useful for libraries than
    applications, so it's probably overkill here, but it takes two
    seconds to code and it protects us against future use as a library.
    '''
