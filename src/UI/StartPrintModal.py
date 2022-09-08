import discord
from discord.ui import Modal, InputText

class StartPrintModal(Modal):
    def __init__(self,  selected_printer_id, callback, *args, **kwargs) -> None:
        super().__init__("Starting Print", *args, **kwargs)
        self.selected_printer_id = selected_printer_id
        self.new_callback = callback
        self.add_item(
            InputText(
                label="Estimated Print Duration",
                placeholder="Time in hours (ex: 7.2)",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await self.new_callback(self.selected_printer_id,
                                interaction.data['components'][0]['components'][0]['value'],
                                interaction)
