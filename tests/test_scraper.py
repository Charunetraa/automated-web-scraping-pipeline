import unittest
from unittest.mock import Mock

from scraper import extract_news


class TestNewsScraper(unittest.TestCase):

    def test_extracts_articles_from_feed(self):
        xml = b"""<?xml version="1.0"?>
        <rss><channel>
          <item>
            <title>Python News</title>
            <link>https://example.com/python</link>
            <pubDate>Mon, 19 Oct 2026 10:00:00 GMT</pubDate>
            <description>Python technology update</description>
          </item>
        </channel></rss>"""

        session = Mock()
        response = Mock()
        response.content = xml
        response.raise_for_status.return_value = None
        session.get.return_value = response

        records = extract_news(session)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["title"], "Python News")
        self.assertEqual(
            records[0]["url"], "https://example.com/python"
        )
        self.assertEqual(records[0]["source"], "BBC Technology")

    def test_removes_duplicate_urls(self):
        xml = b"""<rss><channel>
          <item><title>First</title>
            <link>https://example.com/article</link>
          </item>
          <item><title>Duplicate</title>
            <link>https://example.com/article</link>
          </item>
        </channel></rss>"""

        session = Mock()
        response = Mock()
        response.content = xml
        response.raise_for_status.return_value = None
        session.get.return_value = response

        records = extract_news(session)

        self.assertEqual(len(records), 1)

    def test_sets_empty_optional_fields(self):
        xml = b"""<rss><channel>
          <item><title>Simple News</title>
            <link>https://example.com/simple</link>
          </item>
        </channel></rss>"""

        session = Mock()
        response = Mock()
        response.content = xml
        response.raise_for_status.return_value = None
        session.get.return_value = response

        records = extract_news(session)

        self.assertEqual(records[0]["published_at"], "")
        self.assertEqual(records[0]["description"], "")


if __name__ == "__main__":
    unittest.main()