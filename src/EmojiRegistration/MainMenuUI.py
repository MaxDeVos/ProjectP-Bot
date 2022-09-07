import discord


# Define a simple View that gives us a confirmation menu
from src.EmojiRegistration.NewEmojiUI import NewEmojiModal


class EmojiSelectionView(discord.ui.View):
    def __init__(self, user, parent):
        super().__init__()
        self.bot = parent.bot
        self.value = None
        self.user = user
        self.parent = parent

    @discord.ui.button(label="Upload New Emoji", style=discord.ButtonStyle.green)
    async def uploadNew(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            new_emoji_modal = NewEmojiModal(self.bot, self.user, title="Modal")
            await interaction.response.send_modal(new_emoji_modal)
            self.value = "new"
            self.stop()

    @discord.ui.button(label="Replace Existing Emoji", style=discord.ButtonStyle.primary)
    async def replaceExisting(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "replace"
            self.stop()

    @discord.ui.button(label="Manage Personal Emoji", style=discord.ButtonStyle.secondary)
    async def personal(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "personal"
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "cancel"
            self.stop()
