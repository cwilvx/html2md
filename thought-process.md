# Debian News page to md script — The thought process

Hello 👋

This page documents my thought process for writing the Python script that reads the[ Debian news page](https://wiki.debian.org/News) and saves the page content in a markdown file.

## The Problem

The script needs to do at least these 3 things:

1. Download a page from the internet
2. Convert the page into markdown
3. Save the markdown into a file

## The Approach

In the current age of software programming, it’s hard to come across a problem that has never been encountered by someone else. So, unless this problem was an anomaly, I wasn’t going to reinvent the wheel.

I assumed that there should be some kind of python library/s that can help solve the main problem. ie. converting the page to markdown. I have experience working with HTTP requests and the filesystem on my side project, which means that problems relating to the two were automatically taken care of.

A quick Google search gave me my first library: [`beautifulsoup`](https://pypi.org/project/beautifulsoup4/) which is used to parse HTML. I read through the “quick start” section of the docs and tried the code snippets in the Python shell. It worked as advertised.

I inspected the page on the browser’s dev tools to understand the page layout. I figured out that the page content was enclosed in an element with the id `content` which makes it easier to single it out.

The next part was figuring out how to convert the page into markdown. I Googled “beautifulsoup to markdown” which gave me [`python-markdownify`](https://github.com/matthewwithanm/python-markdownify). I tried the quick start snippets in the Python shell and everything worked fine.

## Putting the Pieces Together

With those two libraries, the requirements for building the script were satisfied. The remaining part was to put all the pieces together to get a working script. This led to[ the initial draft](https://github.com/mungai-njoroge/html2md/commit/9e68f48cd72a45d009f41924c011d0dd9776916c#diff-b10564ab7d2c520cdd0243874879fb0a782862c3c902ab535faabe57d5a505e1) of the script.

The script does the following:

1. Downloads the news page using `requests`
2. Extracts metadata from the page. ie. page title, last updated date and translation links
3. Formats the metadata as a frontmatter string
4. Extracts the content element using `beautifulsoup.find` method
5. Removes unneeded elements from the content
6. Converts it to markdown using `python-markdownify`
7. Finally, saves it to a markdown file.

I then restructured the code to make it easier for people to read, update and maintain, by:

- Extracting actions into functions
- Adding docstrings
- Extracting variables and
- Adding tests.

The final draft of the script can be found in `main.py`. 👇👇

<https://github.com/mungai-njoroge/html2md/blob/main/main.py>

## Writing Tests

Prior to writing the script, I had almost zero experience writing tests in any programming language or framework. I knew what tests are, how they are supposed to look like, but not explicitly written them myself. So I had to read through a couple of guides and documentations on Python tests. I wrote a few dummy scripts that behaved similar to my html-to-md script and used them to learn. I was finally able to write tests for my script.

Here’s what I came up with. 👇👇

<https://github.com/mungai-njoroge/html2md/blob/main/test_main.py>

All the tests are currently passing.

## Challenges

Writing tests was a challenge due to my lack of prior experience. I overcame it by updating my knowledge base through learning how to write tests with the aid of guides. The "[Getting Started With Testing in Python](https://realpython.com/python-testing/)" guide in particular was a life saver.

## Conclusion

The current script is only designed with a single page in mind. To convert the whole debian wiki content to markdown, the script will need to be modified to handle the load.

Some features that could be added include:

### 1. A crawler

To extract all pages in the wiki dynamically without explicitly specifying their url. This can be achieved by recursively:

1. Extracting all links in page
2. Filtering out external links
3. Converting each discovered page

The steps above abstract things like recording seen links, etc.

### 2. Multiprocessing

Processing all the pages in series can take hours. To make it faster, multiprocessing/multithreading can be implemented to allow processing pages in parallel. Assuming we have the current wiki codebase locally and the pages are saved in html, converting them will be fast.

I can’t wait to work on the next part of this project together with the team.

Thank you.
