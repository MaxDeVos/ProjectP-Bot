import discord
from discord.ui import Modal, InputText

class StartPrintModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(
            InputText(
                label="Estimated Print Duration",
                placeholder="Time in hours (ex: 7.2)",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention},{self.children[0].value}")
