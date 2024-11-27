"""A script that scrapes data from the onion website"""

from datetime import datetime
import requests as req
from bs4 import BeautifulSoup

def get_article_details(url:str) -> dict:
    """returns a dict of onion article data"""
    result = req.get(url)

    if result.status_code >= 400:
        raise ValueError("Could not access URL successfully")
    
    onion_soup = BeautifulSoup(result.text, features="html.parser")

    tag_holder = onion_soup.find("div", class_="taxonomy-post_tag")
    tags = tag_holder.find_all("a") if tag_holder else []

    return {"title": onion_soup.find("h1").get_text(),
            "published": datetime.fromisoformat(onion_soup.find("time")["datetime"]),
            "tags": [tag.get_text() for tag in tags]
        }

def get_articles_from_page(url:str) -> list[dict]:
    """Returns a list of all article details on the page"""
    result = req.get(url)

    if result.status_code >= 400:
        raise ValueError("Could not access URL")
    
    onion_soup = BeautifulSoup(result.text, features="html.parser")

    links = onion_soup.find_all("h3")

    articles = []
    for l in links:
        articles.append(get_article_details(l.find("a")["href"]))
    return articles


if __name__ == "__main__":
    # print(get_article_details("https://theonion.com/report-most-americans-have-enough-saved-for-absolutely-incredible-single-day-of-retirement/"))
    print(get_articles_from_page('https://theonion.com/news/page/840/'))
