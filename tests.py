import unittest
import pyninegag
import requests
import logging

logger = logging.getLogger('pyninegag')

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class TestPyNineGag(unittest.TestCase):
    def test_base_url_reachable(self):
        resp = requests.head(pyninegag.BASE_URL)
        resp.raise_for_status()

    def test_get_sections(self):
        sections = pyninegag.get_sections()
        self.assertGreater(len(sections), 0)
        print('Sections: {}'.format(sections))

    def test_get_articles(self):
        articles = pyninegag.get_articles(pyninegag.BASE_URL, max_pages=1, raise_on_error=True)
        articles = list(articles)
        self.assertGreater(len(articles), 0)

        articles_two_pages = pyninegag.get_articles(pyninegag.BASE_URL, max_pages=2, raise_on_error=True)
        articles_two_pages = list(articles_two_pages)
        self.assertGreater(len(articles_two_pages), len(articles))

    def test_get_by_sections(self):
        for section_name in pyninegag.get_sections():
            try:
                next(pyninegag.get_by_section(section_name))
            except StopIteration:
                continue

        with self.assertRaises(ValueError):
            pyninegag.get_by_section('some invalid section name 14512')