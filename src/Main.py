from discord.ext import commands

from src.PinSystem.PinCog import PinCog
from src.Translation.TranslationCog import TranslationCog

# Read API key from file
f = open("data/test_key.txt", "r")
# f = open("data/key.txt", "r")
key = f.read()

active_guild = 782870393517768704


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.guild = None
        self.channelDict = {}
        super().__init__(*args, **kwargs)

    async def on_ready(self):

        for n in self.guilds:
            if n.id == active_guild:
                self.guild = n
                print("Found GUILD: " + self.guild.name)

        for a in self.guild.text_channels:
            self.channelDict[a.name] = a

        print('Ready!')
        bot.add_cog(PinCog(bot, self))
        bot.add_cog(TranslationCog(bot))


bot = Bot()
bot.run(key)
