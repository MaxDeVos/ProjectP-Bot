import logging

from discord import ApplicationContext
from discord.ext import commands

from src import active_guild_id
from src.PrinterStatus.PrinterList import PrinterList
from src.PrinterStatus.StartPrintModal import StartPrintModal
from src.TimestampGenerator import TimestampGenerator

ts = TimestampGenerator("PRINTERS")


class PrinterStatusCog(commands.Cog):

    def __init__(self, bot, parent):
        self.bot = bot
        self.parent = parent
        self.emoji_channel = self.parent.channelDict["emoji-voting"]
        logging.info(f"{ts.get_time_stamp()} Starting Emoji Registration System")

    @commands.slash_command(guild_ids=[active_guild_id])
    async def submit_emoji(self, ctx: ApplicationContext):
        await ctx.send("GAMING", view=PrinterList())
