# html2md
[![Tests](https://github.com/mungai-njoroge/html2md/actions/workflows/run_tests.yml/badge.svg)](https://github.com/mungai-njoroge/html2md/actions/workflows/run_tests.yml)

A python script that reads the [debian news page](https://wiki.debian.org/News) and spits out a markdown file that renders the same page.

## Running it

Clone this repo locally, create a virtual environment, install dependencies and run `main.py`.

```sh
git clone https://github.com/mungai-njoroge/html2md.git

cd html2md
```

If you have [Poetry](https://python-poetry.org) installed:

```sh
poetry install

# run main.py
poetry run python main.py
```

Without Poetry:

```sh
# create virtual environment
python -m venv venv

# activate it
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run script
python main.py
```

## Libraries used

- [requests](https://pypi.org/project/requests/) - Downloading webpage
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Parsing Html into tree structure
- [markdownify](https://github.com/matthewwithanm/python-markdownify) - Generating Markdown from a string

## How it works

The page is fetched using the [requests](https://pypi.org/project/requests/) package and then parsed into a tree structure using [BeautifulSoup](https://pypi.org/project/beautifulsoup4/).

Important information that can be used by a wiki engine is extracted from the page and stored to be used as front matter in the final markdown file.

The relevant section of the webpage is inside the element with id `content`. This section is singled out using the [`BeautifulSoup.find`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find) method. Unneeded elements in the 'content' are identified and removed using the [`BeautifulSoup.decompose`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#decompose) method. The [`markdownify`](https://github.com/matthewwithanm/python-markdownify) package is then used to generate markdown from the remainder.

## Running tests

Tests are defined in the `test_main.py` file. You can run them by running `pytest` (which was installed as a dependency).

```sh
python -m pytest
```

With Poetry:

```sh
poetry run python -m pytest
```
