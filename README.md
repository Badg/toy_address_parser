# Toy address parser

A simple multinational address parser. Simple as in "quick and dirty", not as in "easy to use" (though it's that too I suppose). Not to be used in production. Mostly written for the obvious reasons 😊, but I also wanted to learn a bit. There are some lessons learned in the ["discussion" section](#discussion) down below!

[![CI](https://github.com/Badg/toy_address_parser/workflows/CI/badge.svg)](https://github.com/Badg/toy_address_parser/actions)

## Important notes

+   There are some third-party dependency choices here that I would not necessarily make in production. In particular, though trio itself is (in my opinion) an extremely good project, the trio ecosystem is very fledgeling. I might consider it for production use, but only after a heavy technical discussion with whatever team I was working with. Note that there are some interop tools that makes it easy to work with eg asyncio libraries, but for the extremely simple use I had for it here, they weren't needed.
+   Testing for this is woefully insufficient for production, especially for something as finicky as address parsing. There's been a whole lot of ink spilled about "things developers think they know (but are wrong) about addresses". There's absolutely no way this captures the edge cases.
+   Frankly, I'm not even convinced writing a grammar is the right way of doing this. But it was the most expedient way I personally could implement an address parser, and also gave me an excuse to play around with Lark, which I've been meaning to do for a while
+   I had to time-box myself on this; I really couldn't put in more than a day and a half over a single weekend. Total (wall clock) time was less than 10hrs, including a chunk of time spent reading up on international address formats
+   If I had more time, I'd build a parser using deep learning, trained on the OpenStreetMap dataset. But I've worked with OSM data before and I know it well enought to say there's no way I would have fit that within a single weekend
+   Side note, I'm not sure where they source their training data, but that's basically the idea behind [deepparse](https://deepparse.org/), and **exactly** the [methodology](https://www.mapzen.com/blog/inside-libpostal/) behind [libpostal](https://github.com/openvenues/libpostal), including its python binding, [pypostal](https://github.com/openvenues/pypostal). **If I really needed to do address parsing in prod, I would just use a library to do it!**
+   All of the applications for the parser (the localhost server, the CLI, and the library import) are all manually tested, for time reasons. These are all things you *can* have automated integration tests for, but it's not as simple as the parser, so I cut that for time

## Installation, usage, tests

### With ``poetry``

```bash
# ----- Installation ------
git clone <repo>
poetry install
# ----- Usage ------
# Serves a parser on localhost on <port>; defaults to 8000.
# parse something with http://localhost/parse/<address>
poetry run python -m toy_address_parser serve [port]
# Parses via command line
poetry run python -m toy_address_parser parse "Musterstraße 123"
# ----- Running tests ------
poetry run python -m pytest --import-mode=importlib
```

### With ``pip``

```bash
# ----- Installation ------
git clone <repo>
# In your favorite venv
pip install .
# ----- Usage ------
# Serves a parser on localhost on <port>; defaults to 8000.
# parse something with http://localhost/parse/<address>
python -m toy_address_parser serve [port]
# Parses via command line
python -m toy_address_parser parse "Musterstraße 123"
# ----- Running tests ------
python -m pytest --import-mode=importlib
```

**Note: this requires a relatively new ``pip`` version** (I believe ``19.0.0`` or above, but don't quote me on that; I tested with 19.2.3).

### Usage as a normal python module

First, install however you'd like, for example, ``pip install git+git:///github.com/Badg/toy_address_parser.git``. Now, from inside python:

```python
from toy_address_parser import parse
parse('Musterstraße 123')
```

## Style guide notes

Formatted per pep8 but not pep257. Specifics are in ``.flake8``, but the potentially contentious decisions ones are:

+   Max line length 79 characters
+   Break lines after binary operators, not before ([opinions on this are changing](https://stackoverflow.com/questions/7942586/correct-style-for-line-breaks-when-chaining-methods-in-python/7942617#7942617))
+   Import statements are alphabetized and grouped:
    1.  ``import <stdlib>``
    2.  ``from <stdlib> import <x>``
    3.  (empty line)
    4.  ``import <thirdparty_dep>``
    5.  ``from <thirdparty_dep> import <y>``
    6.  (empty line)
    7.  ``import <internal_dep>``
    8.  ``from <internal_dep> import <z>``
+   Import statements always use full absolute names, eg ``from ghibli_wrapper.utils import <x>``, not ``from .utils import <x>``
+   Docstrings:
    *   Triple single quotes, not triple double (I recognize this is in direct opposition to pep257)
        -   I do this purely for ergonomic reasons
        -   It just occurred to me that in all my years I never really learned to use the left shift, so maybe I'll start changing that
        -   Pre-commit hooks are great for normalizing docstrings anyways
    *   No line break on first line of docstr (``'''Foo...``, not ``'''\nFoo``)
    *   Closing triple quotes on dedicated line
    *   No blank line before closing triple quotes
+   I'm a little inconsistent about how I break brackets and parenthesis when their contents expand beyond a single line. It's partly something I need to work on, and partly something that I don't think fits well aesthetically into python in general

## Discussion

+   This was my first time using Typer, which went super well actually. I think its API is a serious step forward compared to other CLI-making frameworks, though I still have some minor complaints
+   This isn't the first grammar I've written, but it's the first I've written using Lark. My general feeling is that using a formal grammar for address parsing is going to be a game of whack-a-mole. With some relatively quick brute force work, you'll get 85-90% of addresses to parse, but the remaining 10-15%... I think an ML solution would be more accurrate and probably faster to run. But for me personally, it wouldn't have been faster to code, and again, I'm under a lot of time pressure
+   Dealing with potential parse ambiguity would be much, much easier if the country was given in addition to the plain address. Really, any additional information would be helpful here; there's a lot of ambiguity in address formats and it's hard to disambiguate without more info (or an ML solution)
+   One big lesson I learned: it seems like Lark's added sugar into EBNF (in particular, parenthetical groupings) is really fragile, and the Earley algorithm doesn't get insight into it, or... something. So it seems like you're better off avoiding them except for really simple stuff. At any rate, for a brief while I was getting non-deterministic parse results, which... does not lend itself to confidence!
