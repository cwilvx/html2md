# html2md

A python script that reads a webpage and spits out a markdown file that renders the same page.

## Libraries used

- [requests](https://pypi.org/project/requests/) - Downloading webpage
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Parsing Html into tree structure
- [markdownify](https://github.com/matthewwithanm/python-markdownify) - Generating Markdown from a string

## How it works

The page is fetched using the [requests](https://pypi.org/project/requests/) package and then parsed into a tree structure using [BeautifulSoup.](https://pypi.org/project/beautifulsoup4/).

Important information that can be used by a wiki engine are extracted from the page and stored to be used as front matter in the final markdown file.

The relevant section of the webpage is inside the element with id `content`. This section is singled out using the [`BeautifulSoup.find`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find) method. Unneeded elements in the 'content' are identified and removed using the [`BeautifulSoup.decompose`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#decompose) method. The [`markdownify`](https://github.com/matthewwithanm/python-markdownify) package is then used to generate markdown from the remainder.

