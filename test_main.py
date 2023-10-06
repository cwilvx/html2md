import os
import unittest
from unittest.mock import patch, MagicMock

from bs4 import BeautifulSoup

from main import (
    fetch_page,
    get_content,
    get_frontmatter,
    get_md,
    save_to_file,
    debian_news_url,
)


last_updated = "2021-08-01"
page_title = "News"
translations = "<small>Translation links</small>"
frontmatter = f"---\ntitle: {page_title.strip()}\nlast_updated: {last_updated}\n---\n\n"

page_content_html = f'<div id="content"><hr>{translations}<b>Page content</b><hr></div>'

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
    def test_fetch_page_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Hello, world!</h1></body></html>"
        mock_get.return_value = mock_response

        result = fetch_page(debian_news_url)

        self.assertEqual(result, mock_response.text)

    @patch("main.requests.get")
    def test_fetch_page_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(SystemExit):
            fetch_page(debian_news_url + "/404")


class TestGetFrontmatter(unittest.TestCase):
    def test_get_frontmatter(self):
        page = BeautifulSoup(
            page_html,
            "html.parser",
        )

        result = get_frontmatter(page)

        self.assertEqual(
            result,
            frontmatter,
        )


class TestGetContent(unittest.TestCase):
    def test_get_content(self):
        page = BeautifulSoup(
            page_html,
            "html.parser",
        )

        result = get_content(page)
        assert_to = page_content_html.replace(translations, "").replace("<hr>", "")

        self.assertEqual(
            str(result),
            assert_to,
        )


class TestGetMd(unittest.TestCase):
    def test_get_md(self):
        page = BeautifulSoup(page_html, "html.parser")
        content = get_content(page)
        result = get_md(content)

        self.assertEqual(result.strip(), "**Page content**")


class TestSaveToFile(unittest.TestCase):
    def setUp(self):
        self.filepath = "testfile.md"

    def tearDown(self):
        os.remove(self.filepath)

    def test_save_to_file(self):
        content = "Hello, world!"

        save_to_file(self.filepath, content)

        with open(self.filepath, "r") as f:
            result = f.read()

        self.assertEqual(result, content)
