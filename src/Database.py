import discord

# Handles raw database operations. Overwrites and reads database in its entirety.
class Database:

    database_channel: discord.channel.TextChannel

    def __init__(self, bot):
        self.bot = bot
        self.database_channel = self.bot.channelDict["bot-database"]
        self.database_message_id = None

    async def async_init(self):
        history = await self.database_channel.history(limit=None, oldest_first=True).flatten()
        database_message = history[0]
        if not database_message.author.id == self.bot.user.id:  # verify that the head message belongs to the bot
            raise Exception("Database Exception: head message isn't editable")
        self.database_message_id = database_message.id

    async def get_database_content(self, raw=False):
        message = await self.database_channel.fetch_message(self.database_message_id)
        content = message.content
        if not raw:
            content = content.replace("```", "")
        return content

    async def overwrite_database(self, content_to_write, raw=False):
        if not raw:
            content_to_write = f"```{content_to_write}```"
        message = await self.database_channel.fetch_message(self.database_message_id)
        await message.edit(content=content_to_write)