python-ninegag
**************

Python library to get stuff from 9gag.com

Installation
============

Via pip:

.. code-block:: shell

    pip install python-ninegag

Usage
=====

.. code-block:: python

    pyninegag.get_sections()

Returns dict of 9gag sections, where keys are capitalized sections names, and values are their urls.

Example output:

.. code-block:: python

    {'Fresh': 'http://9gag.com/fresh',
    'Cute Animals': 'http://9gag.com/cute',
    'Comic': 'http://9gag.com/comic',
    'Food': 'http://9gag.com/food',
    'GIF': 'http://9gag.com/gif',
    'Cosplay': 'http://9gag.com/cosplay',
    'Geeky': 'http://9gag.com/geeky',
    'Girl': 'http://9gag.com/girl',
    'Funny': 'http://9gag.com/funny',
    'Design': 'http://9gag.com/design',
    'WTF': 'http://9gag.com/wtf',
    'NSFW': 'http://9gag.com/nsfw',
    'Trending': 'http://9gag.com/trending',
    'Timely': 'http://9gag.com/timely',
    'Meme': 'http://9gag.com/meme',
    'Hot': 'http://9gag.com/hot'
    }

NOTE: NSFW section will return zero articles (empty iterable) since watching this section requires user login, which is not supported by this library.

These values are not hardcoded and will be generated on first request. Values are cached.

.. code-block:: python

    pyninegag.get_articles(url, max_pages=1)

Return iterable with all articles found on given url.
``max_pages`` - how many pages of results to parse. If None - all available. Default 1 - only first page.

.. code-block:: python

    pyninegag.get_articles(pyninegag.BASE_URL)

Will return all articles on main 9gag page.

Example output:

.. code-block:: python

    [
    {
        'id': 'a1MEzz6',
        'title': 'Jumping into the abyss',
        'data': {
            'type': 'gif',
            'url': 'http://img-9gag-fun.9cache.com/photo/a1MEzz6_460sa.gif'
        },
        'comments': '163',
        'votes': '10709',
        'url': 'http://9gag.com/gag/a1MEzz6'
    },
    {
        'id': 'agVEP3g',
        'title': 'Made of crab',
        'data': {
            'type': 'image',
            'url': 'http://img-9gag-fun.9cache.com/photo/agVEP3g_700b_v1.jpg'
        },
        'comments': '257',
        'votes': '10053',
        'url': 'http://9gag.com/gag/agVEP3g'
    }
    ]

Article type can be one of gif, image or longpost. Longpost is just a very tall image.

.. code-block:: python

    pyninegag.get_by_section(section_name, max_pages=1)

Return iterable with all articles found in given section. Section name must be one of the keys of ``pyninegag.get_sections()``. If not found, ``ValueError`` will be raised.

There is also a logger ``pyninegag`` enabled that logs exceptions and warnings of parsing errors. All errors contain article id and url in message for easier debugging of problems.
