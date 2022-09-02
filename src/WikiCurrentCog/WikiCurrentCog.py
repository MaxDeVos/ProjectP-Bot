import asyncio
import logging

import discord
from discord.ext import commands

from src.TimestampGenerator import TimestampGenerator
from src.WikiCurrentCog.WikipediaPageParser import WikipediaParser

ts = TimestampGenerator("NEWS")


class WikiCurrentCog(commands.Cog):
    guild: discord.Guild

    def __init__(self, bot, parent):
        self.bot = bot
        self.parent = parent
        self.wiki_parser = WikipediaParser()
        logging.info(f"{ts.get_time_stamp()} Starting Wiki Current Events Cog")
        asyncio.get_event_loop().create_task(self.send_latest_news())

    async def send_latest_news(self):
        for message in self.wiki_parser.get_news_messages():
            await self.parent.channelDict["general"].send(message)
