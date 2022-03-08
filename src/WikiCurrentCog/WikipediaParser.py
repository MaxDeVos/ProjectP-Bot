import asyncio
import datetime as datetime

import requests as requests
from bs4 import BeautifulSoup
from markdownify import markdownify


class WikipediaParser:

    def __init__(self):
        URL = "https://en.wikipedia.org/wiki/Portal:Current_events"
        page = requests.get(URL)

        today_timestamp = datetime.datetime.now()
        today_built_date = today_timestamp.strftime("%Y_%B_%e").replace(" ", "")
        print(today_built_date)

        yesterday_timestamp = today_timestamp - datetime.timedelta(days=1)
        yesterday_built_date = yesterday_timestamp.strftime("%Y_%B_%e").replace(" ", "")
        print(yesterday_built_date)

        soup = BeautifulSoup(page.content, "html.parser")
        today_block = soup.find("div", id=today_built_date).find(class_="current-events-content")
        for a in today_block.findAll('a'):
            del a['href']

        self.categories = today_block.find_all("ul", recursive=False)

    def get_news_messages(self):
        out = []
        for cat in self.categories:
            markdown = markdownify(str(cat))
            out.append(markdown.replace("\n\n\n", "\n").replace("\n\n", "\n"))
        return out
