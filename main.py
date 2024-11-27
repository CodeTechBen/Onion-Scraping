"""A script that scrapes data from the onion website"""

from datetime import datetime
import json
import requests as req
from bs4 import BeautifulSoup
from time import sleep
from rich.progress import Progress

def get_article_details(url:str) -> dict:
    """returns a dict of onion article data"""
    result = req.get(url)

    if result.status_code >= 400:
        raise ValueError("Could not access URL successfully")
    
    onion_soup = BeautifulSoup(result.text, features="html.parser")

    tag_holder = onion_soup.find("div", class_="taxonomy-post_tag")
    tags = tag_holder.find_all("a") if tag_holder else []

    return {"title": onion_soup.find("h1").get_text(),
            "published": onion_soup.find("time")["datetime"],
            # datetime.fromisoformat(onion_soup.find("time")["datetime"]),
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
        sleep(1)
        articles.append(get_article_details(l.find("a")["href"]))
    return articles


if __name__ == "__main__":
    all_articles = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Scraping articles...", total=9 * 12)

        for i in range(1, 10):
            page_articles = get_articles_from_page(
                f'https://theonion.com/news/page/{i}/')
            all_articles.extend(page_articles)
            progress.update(task, advance=len(page_articles))

    with open("onion_articles.json", "w") as f:
        json.dump(all_articles, f, indent=4)
