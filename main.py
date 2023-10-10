import sys

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

debian_news_url = "https://wiki.debian.org/News"
filepath = "debian_news.md"

title_id = "locationline"
pageinfo_id = "pageinfo"
content_id = "content"


def get_md(content, **options):
    """
    Converts a BeautifulSoup4 object to Markdown

    :param content: BeautifulSoup object
    :param options: Markdownify options
    :return: Markdown string
    """
    markdown = MarkdownConverter(**options, heading_style="ATX").convert_soup(content)
    markdown = markdown.strip() + "\n\n"
    return markdown


def fetch_page(url: str):
    """
    Fetches the page content from the given URL
    and returns it as a string. Exits if the request fails.

    :param url: URL of the page to fetch
    :return: Page content as a string
    """
    response = requests.get(url)

    if response.status_code != 200:
        print(
            f"Failed to retrieve the Debian News page. Status code: {response.status_code}"
        )
        sys.exit(1)

    return response.text


def get_translations_frontmatter(page: BeautifulSoup):
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


def get_frontmatter(page: BeautifulSoup):
    """
    Extracts metadata from the page and returns it as a
    frontmatter string.

    :param page: BeautifulSoup object of the page
    :return: Frontmatter string
    """
    translations = get_translations_frontmatter(page)

    page_title = page.find(id=title_id).get_text()
    pageinfo = page.find(id=pageinfo_id).get_text()

    # Extract last updated date from #pageinfo node
    last_updated = pageinfo.split("modified")[1].replace(")", "").strip()

    return f"---\ntitle: {page_title.strip()}\nlast_updated: {last_updated}\n{translations}---\n\n"


def get_content(page: BeautifulSoup):
    """
    Returns the content of the page as a BeautifulSoup object

    :param page: BeautifulSoup object of the page
    :return: BeautifulSoup object of the content
    """
    content = page.find("div", {"id": content_id})

    # remove translation links
    content.find("small").decompose()  # first <small> node

    # find all dt nodes and change them to h3
    for dt in content.find_all("dt"):
        dt.name = "h3"

    # remove first horizontal line
    content.find("hr").decompose()

    return content


def save_to_file(path: str, content: str):
    """
    Saves the content to the given path. Overwrites the file if it exists.

    :param path: Path to the file
    :param content: Content to write
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
        print(f"Wrote {len(content)} bytes to {path}")


class PageToMd:
    """
    Class that orchastrates the conversion of the Debian News page
    """

    def __init__(self, url: str, path: str) -> None:
        html = fetch_page(url)
        page = BeautifulSoup(html, "html.parser")

        frontmatter = get_frontmatter(page)
        content = get_content(page)
        markdown = get_md(content)

        text = frontmatter + markdown
        save_to_file(path, text)


if __name__ == "__main__":
    PageToMd(debian_news_url, filepath)
