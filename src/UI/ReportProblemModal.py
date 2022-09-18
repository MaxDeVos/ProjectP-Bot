import discord
from discord.ui import Modal, InputText

class ReportProblemModal(Modal):
    def __init__(self,  selected_printer_id, callback, *args, **kwargs) -> None:
        super().__init__("Reporting Problem", *args, **kwargs)
        self.selected_printer_id = selected_printer_id
        self.new_callback = callback
        self.add_item(
            InputText(
                label="Problem description",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await self.new_callback(interaction.user,
                                self.selected_printer_id,
                                interaction.data['components'][0]['components'][0]['value'],
                                interaction)
