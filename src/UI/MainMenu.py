import discord
from discord import ButtonStyle, ApplicationContext
from discord.ui import View

from src import PrinterManger
from src.UI.PrinterSelection import StartPrintPrinterSelection
from src.UI.StartPrintModal import StartPrintModal


class MainMenu(View):

    printer_manager: PrinterManger

    def __init__(self, printer_manager):
        super().__init__(timeout=None)
        self.printer_manager = printer_manager



    @discord.ui.button(
        style=ButtonStyle.green,
        label="Started a print",
        custom_id="started-print",
        emoji="🖨️")
    async def started_print_printer_selection(self, button, interaction: ApplicationContext):
        await interaction.response.send_message("Select printer to start print",
                                                view=
                                                StartPrintPrinterSelection(self.printer_manager.get_printer_options(),
                                                                           self.started_print_launch_modal),
                                                ephemeral=True)

    async def started_print_launch_modal(self, selected_printer_id, interaction: ApplicationContext):
        await interaction.response.send_modal(StartPrintModal(selected_printer_id=selected_printer_id,
                                                              callback=self.started_print_process_data))

    async def started_print_process_data(self, selected_printer_id, modal_result, interaction: ApplicationContext):
        print(selected_printer_id, modal_result)
        await interaction.response.send_message("Operation Completed Successfully!", ephemeral=True)



    @discord.ui.button(
        style=ButtonStyle.red,
        label="Cancelled a print",
        custom_id="cancelled-print",
        emoji="✖️")
    async def cancelled_print_callback(self, button, interaction):
        await interaction.response.send_message(f"Button Clicked!")

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
