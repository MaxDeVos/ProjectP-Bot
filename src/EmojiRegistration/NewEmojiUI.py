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
                placeholder="This emoji indicates your orgasmic enjoyment of something",
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
                tempChan: discord.TextChannel
                tempChan = self.bot.channelDict["emoji-upload-cache"]
                image_sent = await tempChan.send(file=discord.File(ip.name + '.png'))

                embed = discord.Embed(title="Emoji Submission Confirmation", color=discord.Color.orange())
                embed.add_field(name="Emoji Name", value=f":{self.children[0].value}:", inline=True)
                embed.add_field(name="Description", value=self.children[1].value, inline=False)
                embed.set_image(url=image_sent.attachments[0].url)
                view = NewEmojiConfirmationView(message.author)

                sent_message = await message.reply(embeds=[embed], view=view)
                await view.wait()
                await sent_message.edit(view=None)

                if view.value is None:
                    await sent_message.reply("I'm done waiting for you.")
                    self.bot.remove_listener(self.on_message)
                if view.value == "confirm":
                    await sent_message.reply(f"Sending :{self.children[0].value}: to a vote now.")
                    self.bot.remove_listener(self.on_message)
                    # voter = EmojiVoter(embed=embed)
                elif view.value == "cancel":
                    await sent_message.reply("Understood and ignored.")
                    self.bot.remove_listener(self.on_message)
                elif view.value == "reupload":
                    await sent_message.reply(f"{self.user.mention}, Please upload another image for :{self.children[0].value}:")


class NewEmojiConfirmationView(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.value = None
        self.user = user

    @discord.ui.button(label="Send to Vote", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "confirm"
            self.stop()

    @discord.ui.button(label="Reupload Image", style=discord.ButtonStyle.blurple)
    async def upload_new(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "reupload"
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "cancel"
            self.stop()
