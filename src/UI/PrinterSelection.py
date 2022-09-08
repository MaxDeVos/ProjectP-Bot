import discord
from discord import SelectOption, ApplicationContext
from discord.ui import View, Item


def read_printers_from_file():
    out = []
    printers = open("printers.txt", "r")
    for line in printers:
        out.append(SelectOption(label=line, value=line))
    return out

class StartPrintPrinterSelection(View):

    def __init__(self, *items: Item):
        super().__init__(*items)

    @discord.ui.select(
        options=read_printers_from_file())
    async def selected_printer_callback(self, selection, interaction: ApplicationContext):
        print(selection)
        await interaction.response.send_message(selection.value)
        # await interaction.response.send_modal(StartPrintModal("Started Print"))


class CancelPrintPrinterSelection(View):

    def __init__(self, *items: Item):
        super().__init__(*items)

    @discord.ui.select(
        options=read_printers_from_file())
    async def selected_printer_callback(self, selection, interaction: ApplicationContext):
        print(selection)
        await interaction.response.send_message(selection.value)
        # await interaction.response.send_modal(StartPrintModal("Started Print"))