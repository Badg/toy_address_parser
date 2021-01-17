# Toy address parser

A simple multinational address parser. Simple as in "quick and dirty", not as in "easy to use" (though it's that too I suppose). Not to be used in production. Mostly written for the obvious reasons 😊, but I also wanted to learn a bit. There are some lessons learned in the ["discussion" section](#discussion) down below!

[![CI](https://github.com/Badg/toy_address_parser/workflows/CI/badge.svg)](https://github.com/Badg/toy_address_parser/actions)

## Important notes

+   There are some third-party dependency choices here that I would not necessarily make in production. In particular, though trio itself is (in my opinion) an extremely good project, the trio ecosystem is very fledgeling. I might consider it for production use, but only after a heavy technical discussion with whatever team I was working with. Note that there are some interop tools that makes it easy to work with eg asyncio libraries, but for the extremely simple use I had for it here, they weren't needed.
+   I had to time-box myself on this; I really couldn't put in more than a day and a half over a single weekend
+   If I had more time, I'd build a parser using deep learning, trained on the OpenStreetMap dataset. But I've worked with OSM data before and I know it well enought to say there's no way I would have fit that within a single weekend
+   Side note, I'm not sure where they source their training data, but that's basically the idea behind [deepparse](https://deepparse.org/), and **exactly** the [methodology](https://www.mapzen.com/blog/inside-libpostal/) behind [libpostal](https://github.com/openvenues/libpostal), including its python binding, [pypostal](https://github.com/openvenues/pypostal)
+   

## Installation, usage, tests

### With ``poetry``

```bash
# ----- Installation ------
git clone <repo>
poetry install
# ----- Usage ------
poetry run python -m toy_address_parser
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
python -m toy_address_parser
# ----- Running tests ------
python -m pytest --import-mode=importlib
```

**Note: this requires a relatively new ``pip`` version** (I believe ``19.0.0`` or above, but don't quote me on that; I tested with 19.2.3).

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
