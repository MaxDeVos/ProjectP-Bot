import os
import sys

from discord.ext import commands

from src import active_guild_id, test_guild_id
from src.EmojiRegistration.EmojiRegistrationCog import EmojiRegistrationCog
from src.PinSystem.PinCog import PinCog
from src.TimestampGenerator import TimestampGenerator
from src.Translation.TranslationCog import TranslationCog
from src.WikiCurrentCog.WikiCurrentCog import WikiCurrentCog

ts = TimestampGenerator("BANE")

production = False
if len(sys.argv) > 1:
    try:
        os.chdir(sys.argv[1])
        production = True
        print(f"{ts.get_time_stamp()} RUNNING IN PRODUCTION")
    except Exception as e:
        pass
else:
    active_guild_id = test_guild_id
    print(f"{ts.get_time_stamp()} RUNNING IN TESTING")


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
                print(f"{ts.get_time_stamp()} Found Guild: {guild.name}")
                break

        # Populate channelDict for future convenience
        for a in self.guild.text_channels:
            self.channelDict[a.name] = a

        # Start cogs
        print(ts.get_time_stamp(), 'Starting Cogs')
        self.add_cog(PinCog(bot, self))
        self.add_cog(TranslationCog(bot))
        # self.add_cog(EmojiRegistrationCog(bot, self))
        # self.add_cog(WikiCurrentCog(bot, self))

        # Send Message
        # ch = await self.fetch_channel(852322660125114398)
        # await ch.send("I'm back, asswipes")

        # Add reaction
        # ch = await self.fetch_channel(852322660125114398)
        # msg = await ch.fetch_message(959300803972190259)
        # await msg.add_reaction("🟠")


# Read API key from file
if production:
    f = open("data/key.txt", "r")
else:
    f = open("data/test_key.txt", "r")
key = f.read()

# Create and start Bane Bot
bot = Bot()
bot.run(key)
