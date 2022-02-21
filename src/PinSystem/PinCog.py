import discord
from discord.ext import commands

from src.PinSystem.PinHandler import PinHandler
from src.PinSystem.TimestampGenerator import TimestampGenerator

ts = TimestampGenerator("PINS")


class PinCog(commands.Cog):
    guild: discord.Guild

    def __init__(self, bot, parent):
        self.bot = bot
        self.parent = parent
        self.pinHandler = None
        print(ts.get_time_stamp(), "Starting Pin Manager")
        self.pinHandler = PinHandler(self.parent.channelDict["pins"], self.parent.guild)

    @commands.slash_command(guild_ids=[782870393517768704])  # Create a slash command for the supplied guilds.
    async def hello(self, ctx):
        await ctx.respond("Hi, this is a slash command from a cog!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):
        if reaction.guild_id == self.parent.guild.id:
            await self.pinHandler.handlePinReaction(reaction, self.parent)
