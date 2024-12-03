
# Programmed by: Pouria Polouk (pouria.polouk@gmail.com)

import os
import sqlite3
import requests
import bs4
import re

conn = sqlite3.connect(os.getcwd() + "\\bookToScrapeDB.sqlite")
conn.execute("delete from book")
conn.commit()

for i in range(1, 11):
    rawData = requests.get("https://books.toscrape.com/catalogue/category/books_1/page-" + str(i) + ".html").content
    content = bs4.BeautifulSoup(rawData, "html.parser")
    article = content.find_all("article", attrs={"class": "product_pod"})
    for book in article:
        link = book.find("h3").findChild("a", attrs={"title": True})
        price = book.find("p", attrs={"class": "price_color"})
        star = book.find("p", attrs={"class": re.compile("^star-rating")})
        img = book.find("img", attrs={"class": "thumbnail"})
        print("Title: " + link['title'])
        print("Price: " + price.text)
        print("Star: " + star['class'][1])
        relativeAddress = img["src"]
        result = re.search("media", relativeAddress)
        pos = result.span()[0]
        bookCoverLink = "https://books.toscrape.com/" + relativeAddress[pos:]
        print("Link (book cover): " + bookCoverLink)

        conn.execute("insert into book values('%s','%s','%s','%s')" \
                     % (str(link['title']).replace("'", "''"), price.text, star['class'][1], bookCoverLink))
        conn.commit()

        print("=========================================================================== " + "Page-" + str(i))

