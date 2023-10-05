import sys

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

debian_news_url = 'https://wiki.debian.org/News'
filepath = 'debian_news.md'

def md(soup, **options):
    """
    Converts a BeautifulSoup4 object to Markdown
    """
    return MarkdownConverter(**options, heading_style="ATX").convert_soup(soup)

# Send an HTTP GET request to fetch the page content
response = requests.get(debian_news_url)

if response.status_code != 200:
    print(f'Failed to retrieve the Debian News page. Status code: {response.status_code}')
    sys.exit(1)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# get text of element with id="locationline"
page_title = soup.find(id="locationline").get_text()
pageinfo = soup.find(id="pageinfo").get_text()

# Extract last updated date from #pageinfo node
last_updated = pageinfo.split("modified")[1].replace(")", "").strip()

# Create frontmatter
frontmatter = f"---\ntitle: {page_title.strip()}\nlast_updated: {last_updated}\n---\n\n"

content = soup.find('div', {'id': 'content'})

# remove translation links
content.find('small').decompose()

# remove lines
for line in content.find_all("hr"):
    line.decompose()

# Write the markdown file
with open(filepath, 'w', encoding='utf-8') as markdown_file:
    markdown = md(content).strip()
    text = frontmatter + markdown + '\n\n'
    markdown_file.write(text)
    print(f'Wrote {len(text)} bytes to {filepath}')
