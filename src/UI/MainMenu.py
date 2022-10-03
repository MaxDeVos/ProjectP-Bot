import discord
from discord import ButtonStyle, ApplicationContext
from discord.ui import View

from src import PrinterManger
from src.Printer import PrinterStatus
from src.UI.PrinterSelection import StartPrintPrinterSelection
from src.UI.ReportProblemModal import ReportProblemModal
from src.UI.StartPrintModal import StartPrintModal

class MainMenu(View):

    printer_manager: PrinterManger

    def __init__(self, cog):
        super().__init__(timeout=None)
        self.printer_manager = cog.printer_manager
        self.start_print_func = cog.start_print_func
        self.cancel_print_func = cog.cancel_print_func
        self.mark_problem_func = cog.mark_problem_func
        self.mark_fixed_func = cog.mark_fixed_func

    # ============= Start Print Menu Tree =============
    @discord.ui.button(
        style=ButtonStyle.green,
        label="Started a print",
        custom_id="started-print",
        emoji="🖨️")
    async def started_print_printer_selection(self, button, interaction: ApplicationContext):
        await interaction.response.send_message("Select printer",
                                                view=
                                                StartPrintPrinterSelection(self.printer_manager.get_printer_options(),
                                                                           self.started_print_launch_modal),
                                                ephemeral=True)

    async def started_print_launch_modal(self, selected_printer_id, interaction: ApplicationContext):
        await interaction.response.send_modal(StartPrintModal(selected_printer_id=selected_printer_id,
                                                              callback=self.started_print_process_data))

    async def started_print_process_data(self, user: discord.User, selected_printer_id, modal_result, interaction: ApplicationContext):
        try:
            hours = float(modal_result)
        except ValueError as e:
            await interaction.response.send_message(f"Invalid input: \"{modal_result}\", please try again", ephemeral=True)
            return

        await interaction.response.send_message("Operation Completed Successfully!", ephemeral=True)
        await self.start_print_func(user, selected_printer_id, hours)

    # ============= Cancel Print Menu Tree =============
    @discord.ui.button(
        style=ButtonStyle.red,
        label="Cancelled a print",
        custom_id="cancelled-print",
        emoji="✖️")
    async def cancel_print_callback(self, button, interaction: ApplicationContext):
        if len(self.printer_manager.get_printer_options(status=PrinterStatus.PRINTING)) > 0:
            await interaction.response.send_message("Select printer",
                                                    view=
                                                    StartPrintPrinterSelection(self.printer_manager.get_printer_options(status=PrinterStatus.PRINTING),
                                                                               self.cancel_print_process_data),
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("No active prints!", ephemeral=True)

    async def cancel_print_process_data(self, selected_printer_id, interaction: ApplicationContext):
        await interaction.response.send_message("Operation Completed Successfully!", ephemeral=True)
        await self.cancel_print_func(selected_printer_id)

    # ============= Report Problem Menu Tree =============
    @discord.ui.button(
        style=ButtonStyle.blurple,
        label="Found a problem",
        custom_id="found-problem",
        emoji="⚠")
    async def report_problem_callback(self, button, interaction: ApplicationContext):
        await interaction.response.send_message("Select printer",
                                                view=
                                                StartPrintPrinterSelection(self.printer_manager.get_printer_options(),
                                                                           self.report_problem_launch_modal),
                                                ephemeral=True)

    async def report_problem_launch_modal(self, selected_printer_id, interaction: ApplicationContext):
        await interaction.response.send_modal(ReportProblemModal(selected_printer_id=selected_printer_id,
                                                              callback=self.report_problem_process_data))

    async def report_problem_process_data(self, user: discord.User, selected_printer_id, modal_result, interaction: ApplicationContext):
        await interaction.response.send_message("Operation Completed Successfully!", ephemeral=True)
        await self.mark_problem_func(user, selected_printer_id, modal_result)

    # ============= Fix Problem Menu Tree =============
    @discord.ui.button(
        style=ButtonStyle.gray,
        label="Fixed a problem",
        custom_id="fixed-problem",
        emoji="🧑‍🔧")
    async def mark_fixed_callback(self, button, interaction: ApplicationContext):
        if len(self.printer_manager.get_printer_options(status=PrinterStatus.DOWN)) > 0:
            await interaction.response.send_message("Select printer",
                                                    view=
                                                    StartPrintPrinterSelection(self.printer_manager.get_printer_options(status=PrinterStatus.DOWN),
                                                                               self.mark_fixed_process_data),
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("No broken printers!", ephemeral=True)

    async def mark_fixed_process_data(self, selected_printer_id, interaction: ApplicationContext):
        await interaction.response.send_message("Operation Completed Successfully!", ephemeral=True)
        await self.mark_fixed_func(selected_printer_id)
