import discord
from discord.ui import Modal, InputText

class StartPrintModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(
            InputText(
                label="Fix description",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention},{self.children[0].value}")
