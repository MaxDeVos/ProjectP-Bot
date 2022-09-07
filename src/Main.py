import logging
import os
import sys
from discord.ext import commands
from datetime import datetime
from src import active_guild_id, test_guild_id
from src.TimestampGenerator import TimestampGenerator

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f'logs/LOG-{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.log'),
        logging.StreamHandler()
    ]
)

production = False
if len(sys.argv) > 1:
    try:
        os.chdir(sys.argv[1])
        production = True
        logging.info("RUNNING IN PRODUCTION")
    except Exception as e:
        logging.error(f"FAILED TO FIND DIRECTORY: {sys.argv[1]}")
else:
    active_guild_id = test_guild_id
    logging.info("RUNNING IN TESTING")

ts = TimestampGenerator("BOT")


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.guild = None
        self.channelDict = {}
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        # Find guild that matches active_guild_id
        # self.guild = [guild for guild in self.guilds if guild.id == active_guild_id]
        for guild in self.guilds:
            if guild.id == active_guild_id:
                self.guild = guild
                logging.info(f"{ts.get_time_stamp()} Found Guild: {guild.name}")
                break

        # Populate channelDict for future convenience
        for a in self.guild.text_channels:
            self.channelDict[a.name] = a

        # Start cogs
        logging.info(f"{ts.get_time_stamp()} Starting Cogs")
        # self.add_cog(EmojiRegistrationCog(bot, self))

        # Send Message
        # ch = await self.fetch_channel(852322660125114398)
        # await ch.send("I'm back, asswipes")

        # Add reaction
        # ch = await self.fetch_channel(852322660125114398)
        # msg = await ch.fetch_message(959300803972190259)
        # await msg.add_reaction("🟠")


# Read API key from file
if production:
    f = open("key.txt", "r")
else:
    f = open("test_key.txt", "r")
key = f.read()

# Create and start Bane Bot
bot = Bot()
bot.run(key)
