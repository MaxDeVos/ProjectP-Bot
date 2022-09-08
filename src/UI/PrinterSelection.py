import discord
from discord import SelectOption, ApplicationContext, SelectMenu, Interaction
from discord.ui import View, Item, Select


def read_printers_from_file():
    out = []
    printers = open("printers.txt", "r")
    for line in printers:
        out.append(SelectOption(label=line, value=line))
    return out

class PrinterSelection(Select):
    def __init__(self, options, callback):
        super().__init__()
        self.options = options
        self.new_callback = callback

    async def callback(self, interaction: Interaction):
        await self.new_callback(interaction.data['values'][0], interaction)


class StartPrintPrinterSelection(View):

    def __init__(self, options, callback, *items: Item):
        super().__init__(*items)
        self.add_item(PrinterSelection(options=options, callback=callback))


class CancelPrintPrinterSelection(View):

    def __init__(self, *items: Item):
        super().__init__(*items)

    @discord.ui.select(
        options=read_printers_from_file())
    async def selected_printer_callback(self, selection, interaction: ApplicationContext):
        print(selection)
        await interaction.response.send_message(selection.value)
        # await interaction.response.send_modal(StartPrintModal("Started Print"))