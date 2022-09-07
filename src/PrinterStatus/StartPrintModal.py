import discord
from discord.ui import Modal, InputText

from src.PrinterStatus.PrinterList import PrinterList


class StartPrintModal(Modal):
    InputText
    def __init__(self, bot, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.user = user
        self.add_item(
            InputText(
                label="Print Duration",
                placeholder="Time in hours (ex: 7.2)",
                style=discord.InputTextStyle.short,
            )
        )
        self.to_components().append(PrinterList())

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, Please upload an image for :{self.children[0].value}:, say \"cancel\" to cancel.")