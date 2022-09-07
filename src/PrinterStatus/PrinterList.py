import discord
from discord import SelectMenu, Option, SelectOption
from discord.ui import View


def read_printers_from_file():
    out = []
    printers = open("printers.txt", "r")
    for line in printers:
        out.append(SelectOption(label=line, value=line))
    return out


class PrinterList(View):
    @discord.ui.select(
        options=read_printers_from_file(),
        placeholder="Select Printer")
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")