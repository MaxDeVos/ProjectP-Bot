import logging

import discord.types.channel
from discord import ApplicationContext, bot
from discord.ext import commands

from src import active_guild_id
from src.PrinterStatus.MainMenu import MainMenu
from src.PrinterStatus.StartPrintModal import StartPrintModal
from src.TimestampGenerator import TimestampGenerator

ts = TimestampGenerator("PRINTERS")


class PrinterStatusCog(commands.Cog):

    printer_channel: discord.channel.TextChannel

    def __init__(self, _bot, parent):
        self.bot = _bot
        self.parent = parent
        self.printer_channel = self.parent.channelDict["printer-status"]
        logging.info(f"{ts.get_time_stamp()} Starting Printer Status System")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "test" in message.content:
            await self.printer_channel.send("I have...", view=MainMenu())
