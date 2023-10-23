import logging
import sys
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H2D")

DOMAIN = "https://wiki.debian.org"
DEBIAN_NEWS_URL = DOMAIN + "/News"
FILEPATH = "debian_news.md"

TITLE_ID = "locationline"
PAGEINFO_ID = "pageinfo"
CONTENT_ID = "content"


class OpenFile:
    """
    A class that opens a file and returns a file object. Closes the file automatically
    when the context is exited.
    """

    def __init__(self, path: str, mode: str = "w", encoding: str = "utf-8") -> None:
        """
        Initializes the class with the file path, mode and encoding.

        :param path: Path to the file
        :param mode: File mode (default: "w")
        :param encoding: File encoding (default: "utf-8")
        """
        self.path = path
        self.mode = mode
        self.encoding = encoding

    def __enter__(self):
        """
        Opens the file and returns the file object.

        :return: File object
        """
        self.file = open(self.path, self.mode, encoding=self.encoding)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the file when the context is exited.
        """
        self.file.close()


class PageToMd:
    """
    Converts a Debian News page to Markdown and saves it to a file.
    """

    def __init__(self, url: str = None, path: str = None) -> None:
        """
        Initializes the class and starts the conversion process.

        :param url: URL of the page to convert
        :param path: Path to the file to write
        """
        self.url = url
        self.path = path

    def get_md(self, content: BeautifulSoup, **options: Dict[str, Any]) -> str:
        """
        Converts a BeautifulSoup4 object to Markdown

        :param content: BeautifulSoup object
        :param options: Markdownify options
        :return: Markdown string
        """
        markdown = MarkdownConverter(**options, heading_style="ATX").convert_soup(
            content
        )
        markdown = markdown.strip() + "\n\n"
        return markdown

    def fetch_page(self, url: str) -> str:
        """
        Fetches the page content from the given URL
        and returns it as a string. Raises an exception if the request fails.

        :param url: URL of the page to fetch
        :return: Page content as a string
        """

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to the internet!")
            sys.exit(1)

        if response.status_code != 200:
            logger.error(
                f"Failed to retrieve the Debian News page. Status code: {response.status_code}"
            )
            sys.exit(1)

        return response.text

    def get_translations_frontmatter(self, page: BeautifulSoup) -> str:
        """
        Extracts the translation links from the page and returns them as a
        frontmatter string.

        :param page: BeautifulSoup object of the page
        :return: Frontmatter entry string
        """
        translations_node = page.find("small")
        translations = []

        # for each a tag in the translations node, extract the href + text
        for link in translations_node.find_all("a"):
            href = link.get("href")
            text = link.get_text()
            translations.append(f"  - {text}: {href}")

        # format the translations list as a frontmatter list entry
        translations = "\n".join(translations)
        return f"translations:\n{translations}\n"

    def get_frontmatter(self, page: BeautifulSoup) -> str:
        """
        Extracts metadata from the page and returns it as a
        frontmatter string.

        :param page: BeautifulSoup object of the page
        :return: Frontmatter string
        """
        translations = self.get_translations_frontmatter(page)

        page_title = page.find(id=TITLE_ID).get_text()
        pageinfo = page.find(id=PAGEINFO_ID).get_text()

        # Extract last updated date from #pageinfo node
        last_updated = pageinfo.split("modified")[1].replace(")", "").strip()

        return f"---\ntitle: {page_title.strip()}\nlast_updated: {last_updated}\n{translations}---\n\n"

    def get_content(self, page: BeautifulSoup) -> BeautifulSoup:
        """
        Returns the content of the page as a BeautifulSoup object

        :param page: BeautifulSoup object of the page
        :return: BeautifulSoup object of the content
        """
        content = page.find("div", {"id": CONTENT_ID})

        # remove translation links
        content.find("small").decompose()  # first <small> node

        # find all dt nodes and change them to h3
        for dt in content.find_all("dt"):
            dt.name = "h3"

        # remove first horizontal line
        content.find("hr").decompose()

        return content

    def save_to_file(self, path: str, content: str) -> None:
        """
        Saves the content to the given path. Overwrites the file if it exists.

        :param path: Path to the file
        :param content: Content to write
        """
        with OpenFile(path) as file:
            file.write(content)
            logger.info(f"Wrote {len(content)} bytes to {path}")

    def format_internal_links(self, page: BeautifulSoup) -> BeautifulSoup:
        """
        Formats internal links to be relative to the current page.
        """
        for link in page.find_all("a"):
            href = link.get("href")
            if href.startswith("/"):
                link["href"] = DOMAIN + href

        return page

    def run(self):
        """
        Runs the conversion process.
        """
        html = self.fetch_page(self.url)
        page = BeautifulSoup(html, "html.parser")
        page = self.format_internal_links(page)

        frontmatter = self.get_frontmatter(page)
        content = self.get_content(page)
        markdown = self.get_md(content)

        text = frontmatter + markdown
        self.save_to_file(self.path, text)


if __name__ == "__main__":
    try:
        converter = PageToMd(DEBIAN_NEWS_URL, FILEPATH)
        converter.run()
    except Exception as e:
        logger.exception(e)
