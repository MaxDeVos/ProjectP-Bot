from discord import SelectOption

from src import Printer
from src.Printer import PrinterStatus


async def load_printers(database_content, bot):
    out = []
    printers = await database_content
    for line in printers.split("\n"):
        out.append(Printer.get_printer_from_database(line, bot))
    return out

class PrinterManager:

    def __init__(self, bot):
        self.status_message_id = None
        self.bot = bot
        self.printers = {}

    async def load_printers(self, database_content):
        self.printers = {}
        for printer in await load_printers(database_content, self.bot):
            self.printers[printer.id] = printer

    async def get_formatted_message(self):
        printers = {0: [], 1: [], 2: []}

        for printer in self.printers.values():
            printers[printer.status.value].append(printer)

        printers[0] = sorted(printers[0], key=lambda x: x.name)
        printers[1] = sorted(printers[1], key=lambda x: x.name)
        printers[2] = sorted(printers[2], key=lambda x: x.name)

        out = ""
        for i in range(3):
            for printer in printers[i]:
                formatted_line = await printer.get_formatted_output()
                out = f"{out}{formatted_line}\n"
            out = f"{out}\n"

        return out

    def get_database_message(self):
        out = ""
        for printer in self.printers.values():
            out = f"{out}{str(printer)}\n"
        return out

    def get_printer_options(self):
        options = []
        for printer in self.printers.values():
            options.append(SelectOption(label=f"{printer.name} ({printer.model})", value=printer.id))
        return options
