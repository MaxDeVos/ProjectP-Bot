from discord.ext import commands
from src.Translation.TranslationCog import TranslationCog

# Read API key from file
f = open("data/test_key.txt", "r")
# f = open("data/key.txt", "r")
key = f.read()


bot = commands.Bot()
bot.add_cog(TranslationCog(bot))
bot.run(key)