import logging

import discord.types.channel
from discord import Message, ApplicationContext
from discord.ext import commands

from src.Database import Database
from src.PrinterManger import PrinterManager
from src.UI.MainMenu import MainMenu
from src.TimestampGenerator import TimestampGenerator

ts = TimestampGenerator("PRINTERS")

class PrinterStatusCog(commands.Cog):

    printer_channel: discord.channel.TextChannel
    database_channel: discord.channel.TextChannel

    def __init__(self, _bot):
        self.bot = _bot
        self.printer_manager = None
        self.status_message = None
        self.printer_channel = None
        self.database_channel = None
        self.database = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("ON READY IN COG")
        self.printer_manager = PrinterManager(self.bot)
        self.printer_channel = self.bot.channelDict["printer-status"]
        self.database_channel = self.bot.channelDict["bot-database"]
        self.database = Database(self.bot)

        logging.info(f"{ts.get_time_stamp()} Starting Printer Status System")
        self.bot.add_application_command(self.new_status_messages)
        logging.info("Registered test slash command")

        history = await self.printer_channel.history(oldest_first=True, limit=1).flatten()
        self.status_message = history[0]
        await self.database.async_init()
        await self.regenerate_all()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id == self.database_channel.id and message.author.id == 155102908281520129:
            await self.handle_user_database_update(message=message)

    async def handle_user_database_update(self, message: Message):
        logging.info(f"{ts.get_time_stamp()} Updating database by manual user request.")
        await self.database.overwrite_database(content_to_write=message.content, raw=True)
        await self.regenerate_all()

    async def regenerate_all(self, new_messages=False):
        await self.printer_manager.load_printers(self.database.get_database_content())
        content = await self.printer_manager.get_formatted_message()

        if new_messages:
            self.status_message = await self.printer_channel.send(content)
            await self.printer_channel.send("I have...", view=MainMenu(self.printer_manager))
            return

        status_message = await self.printer_channel.fetch_message(self.status_message.id)
        await status_message.edit(content=content)
        self.bot.add_view(MainMenu(self.printer_manager))

    @commands.slash_command(name="new_status_messages")
    async def new_status_messages(self, ctx: ApplicationContext):
        await self.regenerate_all(new_messages=True)
        await ctx.send_response("GAMING", view=MainMenu(self.printer_manager))
