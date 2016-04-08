import logging
import re
from bs4 import BeautifulSoup

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


LONGPOST_HEIGHT_MIN = 1000
BASE_URL = 'http://9gag.com/'

_sections = None

logger = logging.getLogger('pyninegag')


class NineGagError(Exception): pass


class UnknownArticleType(NineGagError): pass


class NotSafeForWork(NineGagError): pass


def _get_url(url):
    return urlopen(url).read()


def _bs_from_response(response):
    """
    Returns BeautifulSoup from given str with html inside.

    :param str:
    :rtype: bs4.BeautifulSoup
    """
    return BeautifulSoup(response, "html.parser")


def _bs_from_url(url):
    """
    Returns BeautifulSoup from given url.
    Shortcut function.

    :param str url:
    :rtype: bs4.BeautifulSoup
    """
    return _bs_from_response(_get_url(url))


def get_sections():
    """
    Return dict of 9gag sections, where keys are capitalized sections names, and values are their urls.
    Caches returning value.

    :rtype: dict
    """
    global _sections
    if _sections is None:
        bs = _bs_from_url(BASE_URL)
        l = bs.find(attrs='nav-menu').find(attrs='primary').find_all('li')[1:-1]
        l.extend(bs.find_all(attrs="badge-section-menu-items"))
        _sections = dict((i.a.text.strip(), i.a['href']) for i in l)
    return _sections


def _get_articles(url):
    bs = _bs_from_url(url)
    return bs.find_all('article')


def _get_gif(container):
    """
    Return dict with key url that will contain url to source gif and type with value "gif".

    :param bs4.Tag container:
    :rtype: dict
    """
    tag = container.find(attrs='badge-animated-container-animated')
    if not tag:
        return None
    return {'url': tag['data-image'], 'type': 'gif'}


def _get_image(container):
    """
    Return dict with key url that will contain url to source image and type with value image,
    if source image height is below 1000, or longpost, otherwize.

    :param bs4.Tag container:
    :rtype: dict
    """
    tag = container.find(attrs='badge-item-img')
    if not tag:
        return None

    style = container.a['style']
    match = re.search(r'[\d\.]+', style)
    if not match:
        return
    height = float(match.group())

    type = 'image'
    if height > LONGPOST_HEIGHT_MIN:
        type = 'longpost'

    url = urlparse.urljoin(BASE_URL, container.a['href'])

    bs = _bs_from_url(url)
    tag = bs.find(attrs='badge-item-img')

    return {'url': tag['src'], 'type': type}


def _get_data(article):
    """
    Return article data. Returns dict with keys url and type.

    :param bs4.Tag article:
    :rtype: dict|None
    """
    container = article.find(attrs='badge-post-container')
    if container is None:
        raise NotSafeForWork()
    return _get_gif(container) or _get_image(container)


def _parse_article(article):
    """
    Return parsed article data. Supported keys: id, url, votes, comments, title, data.

    :param bs4.Tag article:
    :rtype: dict|None
    """
    data = dict()
    data['id'] = article['data-entry-id']
    data['url'] = article['data-entry-url']
    data['votes'] = article['data-entry-votes']
    data['comments'] = article['data-entry-comments']
    data['title'] = article.find(attrs='badge-item-title').a.text.strip()
    try:
        data['data'] = _get_data(article)
    except Exception as e:
        logger.exception('Error while parsing data of {}: {}'.format(data['id'], data['url']))
        return
    if not data['data']:
        logger.warning('Unknown article type of {}: {}'.format(data['id'], data['url']))
        return
    return data


def get_articles(url):
    """
    Return iterable with all articles found on given url.

    :param str url:
    :rtype: collections.Iterable[dict]
    """
    for article in _get_articles(url):
        try:
            data = _parse_article(article)
            if not data:
                continue
            else:
                yield data
        except Exception as e:
            logger.exception('Error while parsing article')


def get_by_section(section_name):
    """
    Return iterable with all articles found in given section.

    :param str section_name:
    :rtype: collections.Iterable[dict]
    """
    sections = get_sections()
    section_name = section_name.strip().lower().capitalize()
    if section_name not in sections:
        raise ValueError('Invalid section name. Should be one of: {}'.format(list(sections.keys())))
    return get_articles(sections[section_name])
