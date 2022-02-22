import discord
from discord.ui import Modal, InputText

from src.EmojiRegistration.ImageProcessor import ImageProcessor


class NewEmojiModal(Modal):
    def __init__(self, bot, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.user = user
        self.add_item(InputText(label="Emoji Name", placeholder="emoji_name"))
        self.add_item(
            InputText(
                label="Emoji Description",
                value="This emoji indicates your orgasmic enjoyment of something",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, Please upload an image for :{self.children[0].value}:, say \"cancel\" to cancel.")
        self.bot.add_listener(self.on_message)

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:
            if message.content.lower().__contains__("cancel"):
                self.bot.remove_listener(self.on_message)
                await message.reply("Cancelled")
            elif len(message.attachments) == 0:
                await message.reply("Please upload an image. Say \"cancel\" to cancel.")
            else:
                ip = ImageProcessor(message.attachments[0], self.children[0].value)
                await ip.downscale_skew()
                await message.reply(file=discord.File(ip.name + '.png'))
