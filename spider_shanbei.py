#/usr/bin/env python
# encoding=utf8

# updates:
#   2016y 02m 03d
#   created by Snowstar( SnowstarCyan@gmail.com )
#
#   a spider to catch 'shan bei words'.
#   ps: make for learning english... = =#
#

###############################################################################
# import

from bs4 import BeautifulSoup
from math import ceil
from Tkinter import Tk
from urllib2 import urlopen
import sys

###############################################################################
# correct encoding problems on windows
reload(sys)
sys.setdefaultencoding('utf-8')

###############################################################################
# function level 6


def httpget(url):
    html = False
    while not html:
        print url
        html = urlopen(url).read()
    return html

###############################################################################
# function level 5


def solveUnitPage(html):
    soup = BeautifulSoup(html, "html.parser")
    words = [x.text for x in soup("td", class_="span2")]
    means = [x.text for x in soup("td", class_="span10")]
    means = [x.replace('\r\n', " // ").replace('\n', " // ") for x in means]
    cword = int(soup("span", id="wordlist-num-vocab")[0].text)
    cpage = int(ceil(cword / 20.0))
    lsPages = range(int(cpage))

    return words, means, [x + 1 for x in lsPages]


def mergeList(a, b):
    assert(len(a) == len(b))
    return [[a[x], b[x]] for x in range(len(a))]

###############################################################################
# function level 4


def flip(tab):
    return map(list, zip(*tab))


def getUnitContext(url):
    words, means, lsPages = solveUnitPage(httpget(url))
    wtom = mergeList(words, means)
    # htmls = [httpget("%s?page=%d" % (url, page)) for page in lsPages[1:]]
    # for words, means, lsPages in [solveUnitPage(x) for x in htmls]:
    #     wtom += mergeList(words, means)
    return "\n".join([" | ".join(x) for x in wtom])

###############################################################################
# function level 3


def solveBookPage(html):
    soup = BeautifulSoup(html, "html.parser")
    info = soup(class_="wordbook-basic-info")[0]
    title = info("a")[0].text
    lsunit = soup(class_="wordbook-containing-wordlist")
    lsurl = ["http://www.shanbay.com" + x("a")[0]["href"] for x in lsunit]
    lsname = [x(class_="wordbook-wordlist-name")[0].text for x in lsunit]
    lsnumtext = [x(class_="wordbook-wordlist-count")[0].text for x in lsunit]
    lsnum = [int(x[5:].strip()) for x in lsnumtext]
    lscpage = [int(ceil(x / 20.0)) for x in lsnum]

    lsUnitPages = flip([lsname, lsurl, lscpage])
    #
    # [title, [unit_name, [unit_links...]]...]
    #
    lsTitleToPage = [title, [
        [x[0]] +
        [
            [x[1]] +
            ["%s?page=%d" % (x[1], y + 1) for y in range(1, x[2])]
        ]
        for x in lsUnitPages]]

    return lsTitleToPage


def flat(node):
    return sum(map(flat, node), []) if isinstance(node, list) else [node]


def makeContext(url):
    if not url.startswith('http'):
        return url
    return getUnitContext(url)

###############################################################################
# function level 2


def splitBooks(books):
    return filter(lambda x: len(x) > 0, books.split('\n'))


def getBookWordList(book):
    titleToUnits = solveBookPage(httpget(book))
    flatUnits = flat(titleToUnits)

    lsTexted = [makeContext(x) for x in flatUnits[:]]
    text = "\n".join(lsTexted)
    return text


def setclip(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.destroy()


def append_to_file(path_output):
    def append_to(text):
        f = open(path_output, "ab")
        f.write(text)
        f.close()
    return append_to

###############################################################################
# function level 1


def start(books, func_output):
    # if something get wrong, it will not be output...
    lsBooks = splitBooks(books)
    lsBooksText = [getBookWordList(book) for book in lsBooks[:]]
    text = ("\n" * 6).join(lsBooksText)

    func_output(text)

###############################################################################

if __name__ == "__main__":
    books = (
        "http://www.shanbay.com/wordbook/100804/\n"  # 必修1
        # "http://www.shanbay.com/wordbook/100810/\n"  # 必修2
        # "http://www.shanbay.com/wordbook/100813/\n"  # 必修3
        # "http://www.shanbay.com/wordbook/100849/\n"  # 必修4
        # "http://www.shanbay.com/wordbook/100864/\n"  # 必修5
        # "http://www.shanbay.com/wordbook/100936/\n"  # 选修6
        # "http://www.shanbay.com/wordbook/100933/\n"  # 选修7
        # "http://www.shanbay.com/wordbook/100945/\n"  # 选修8
        # "http://www.shanbay.com/wordbook/100930/\n"  # 选修9
        # "http://www.shanbay.com/wordbook/101038/\n"  # 选修10
        # "http://www.shanbay.com/wordbook/100954/\n"  # 选修11
    )
    # you can choose one method to output
    #
    # start(books, setclip)
    start(books, append_to_file("spider_shanbei_WORDS.txt"))
