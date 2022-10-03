import logging
import sys

from discord.ext import commands
from datetime import datetime

sys.path.insert(1, '')

from IDs import active_guild_id
from PrinterStatusCog import PrinterStatusCog
from TimestampGenerator import TimestampGenerator

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f'logs/LOG-{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.log', encoding="utf8"),
        logging.StreamHandler()
    ]
)

production = False
# if len(sys.argv) > 1:
#     try:
#         os.chdir(sys.argv[1])
#         production = True
#         logging.info("RUNNING IN PRODUCTION")
#     except Exception as e:
#         logging.error(f"FAILED TO FIND DIRECTORY: {sys.argv[1]}")
# else:
#     active_guild_id = test_guild_id
#     logging.info("RUNNING IN TESTING")

ts = TimestampGenerator("BOT")


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.debug_guilds = [active_guild_id]
        self.guild = None
        self.channelDict = {}
        super().__init__(*args, **kwargs)

    def load_cogs(self):
        # Start cogs
        logging.info(f"{ts.get_time_stamp()} Starting Cogs")
        printer_cog = PrinterStatusCog(self)
        self.add_cog(printer_cog)

    async def on_ready(self):
        # Find guild that matches active_guild_id
        # self.guild = [guild for guild in self.guilds if guild.id == active_guild_id]
        for guild in self.guilds:
            print(guild)
            if guild.id == active_guild_id:
                self.guild = guild
                logging.info(f"{ts.get_time_stamp()} Found Guild: {guild.name}")
                break

        # Populate channelDict for future convenience
        for a in self.guild.text_channels:
            self.channelDict[a.name] = a



        # Send Message
        # ch = await self.fetch_channel(1017179127066927124)
        # content = open("printers.txt", "r").read()
        # await ch.send(f"```{content}```")

        # Add reaction
        # ch = await self.fetch_channel(852322660125114398)
        # msg = await ch.fetch_message(959300803972190259)
        # await msg.add_reaction("🟠")


# Read API key from file
if production:
    f = open("keys/key.txt", "r")
else:
    f = open("keys/test_key.txt", "r")
key = f.read()

# Create and start Bane Bot
bot = Bot()
bot.load_cogs()
bot.run(key)
# bot.load_extension("src.PrinterStatus.PrinterStatusCog")
# bot.extensions.items().


