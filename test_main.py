import os
import unittest
from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup

from main import DEBIAN_NEWS_URL, DOMAIN, OpenFile, PageToMd

last_updated = "2021-08-01"
page_title = "News"
translations = '<small><a href="/uk/News">Українська</a> - <a href="/vi/News">tiếng Việt</a></small>'
frontmatter = f"---\ntitle: {page_title.strip()}\nlast_updated: {last_updated}\ntranslations:\n  - Українська: /uk/News\n  - tiếng Việt: /vi/News\n---\n\n"

page_content_html = (
    f'<div id="content"><hr/>{translations}<b>Page content</b><hr/></div>'
)
page_html = f"""
<html>
<body>
    <div id="locationline">{page_title}</div>
    {page_content_html}
    <div id="pageinfo">(Last modified {last_updated})</div>
</body>
</html>
"""


class TestFetchPage(unittest.TestCase):
    @patch("main.requests.get")
    def test_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Hello, world!</h1></body></html>"
        mock_get.return_value = mock_response

        result = PageToMd().fetch_page(DEBIAN_NEWS_URL)

        self.assertEqual(result, mock_response.text)

    @patch("main.requests.get")
    def test_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(SystemExit):
            PageToMd().fetch_page(DEBIAN_NEWS_URL + "/404")


class TestGetFrontmatter(unittest.TestCase):
    def runTest(self):
        page = BeautifulSoup(
            page_html,
            "html.parser",
        )

        result = PageToMd().get_frontmatter(page)

        self.assertEqual(
            result,
            frontmatter,
        )


class TestGetContent(unittest.TestCase):
    def runTest(self):
        page = BeautifulSoup(
            page_html,
            "html.parser",
        )

        result = PageToMd().get_content(page)
        assert_to = page_content_html.replace(translations, "").replace("<hr/>", "", 1)

        self.assertEqual(
            str(result),
            assert_to,
        )


class TestGetMd(unittest.TestCase):
    def runTest(self):
        page = BeautifulSoup(page_html, "html.parser")
        content = PageToMd().get_content(page)
        result = PageToMd().get_md(content)

        self.assertEqual(result.strip(), "**Page content**\n\n---")


class TestSaveToFile(unittest.TestCase):
    def setUp(self):
        self.filepath = "testfile.md"

    def tearDown(self):
        os.remove(self.filepath)

    def runTest(self):
        content = "Hello, world!"

        PageToMd().save_to_file(self.filepath, content)

        with open(self.filepath, "r") as f:
            result = f.read()

        self.assertEqual(result, content)


class TestFormatInterlLinks(unittest.TestCase):
    def runTest(self):
        test_node_html = '<small><a href="/uk/News">Українська</a></small>'
        test_node = BeautifulSoup(
            test_node_html,
            "html.parser",
        )

        result = str(PageToMd().format_internal_links(test_node)).strip()
        should_be = test_node_html.replace("/uk/News", DOMAIN + "/uk/News")

        self.assertEqual(result, should_be)


class TestOpenFile(unittest.TestCase):
    def setUp(self):
        self.filepath = "testfile.txt"

    def tearDown(self):
        os.remove(self.filepath)

    def runTest(self):
        content = "Hello, Debian!"

        with OpenFile(self.filepath) as f:
            f.write(content)

        self.assertTrue(f.closed)
