from discord import ApplicationContext
from discord.ext import commands

from src import active_guild_id
from src.EmojiRegistration.MainMenuUI import EmojiSelectionView
from src.EmojiRegistration.NewEmojiUI import NewEmojiModal
from src.PinSystem.TimestampGenerator import TimestampGenerator

ts = TimestampGenerator("EMOJ")


class EmojiRegistrationCog(commands.Cog):

    def __init__(self, bot, parent):
        self.bot = bot
        self.parent = parent
        self.emoji_channel = self.parent.channelDict["emoji-voting"]
        print(ts.get_time_stamp(), "Starting Emoji Registration System")

    @commands.slash_command(guild_ids=[active_guild_id])
    async def submit_emoji(self, ctx: ApplicationContext):
        view = EmojiSelectionView(ctx.user, self)
        fetched_message = await ctx.respond("What would you like to do?", view=view)

        # Wait for the View to stop listening for input...
        await view.wait()
        await fetched_message.edit_original_message(view=None)

