import discord
from discord import SelectOption, ButtonStyle, ApplicationContext
from discord.ui import View

from src.PrinterStatus.StartPrintModal import StartPrintModal


def read_printers_from_file():
    out = []
    printers = open("printers.txt", "r")
    for line in printers:
        out.append(SelectOption(label=line, value=line))
    return out


class MainMenu(View):
    @discord.ui.button(
        style=ButtonStyle.green,
        label="Started a print",
        custom_id="started-print",
        emoji="🖨️")
    async def started_print_callback(self, button, interaction: ApplicationContext):
        await interaction.response.send_modal(StartPrintModal("Start Print"))

    @discord.ui.button(
        style=ButtonStyle.red,
        label="Cancelled a print",
        custom_id="cancelled-print",
        emoji="✖️")
    async def cancelled_print_callback(self, button, interaction):
        await interaction.send_modal.send_message(f"Button Clicked!")

    @discord.ui.button(
        style=ButtonStyle.blurple,
        label="Found a problem",
        custom_id="found-problem",
        emoji="⚠")
    async def report_problem_callback(self, button, interaction):
        await interaction.response.send_message(f"Button Clicked!")

    @discord.ui.button(
        style=ButtonStyle.gray,
        label="Fixed a problem",
        custom_id="fixed-problem",
        emoji="🧑‍🔧")
    async def mark_resolved_callback(self, button, interaction):
        await interaction.response.send_message(f"Button Clicked!")
