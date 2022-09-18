from discord import SelectOption

from src import Printer
from src.Printer import PrinterStatus


async def load_printers(database_content, bot):
    out = []
    printers = await database_content
    for line in printers.split("\n"):
        if line != "":
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
        categories = {0: [], 1: [], 2: []}

        for printer in self.printers.values():
            categories[printer.status.value].append(printer)

        categories[0] = sorted(categories[0], key=lambda x: x.name)
        categories[1] = sorted(categories[1], key=lambda x: x.name)
        categories[2] = sorted(categories[2], key=lambda x: x.name)

        out = "```"
        for i in range(3):
            for printer in categories[i]:
                formatted_line = await printer.get_formatted_output()
                out = f"{out}{formatted_line}\n"
            out = f"{out}\n"

        return f"{out}```"

    def get_database_message(self):
        out = ""
        for printer in self.printers.values():
            out = f"{out}{str(printer)}\n"
        return out

    def get_printer_options(self, status=None):
        options = []
        _printers = []
        for printer in self.printers.values():
            if status is None or status == printer.status:
                _printers.append(printer)

        _printers = sorted(_printers, key=lambda x: x.name)

        for printer in _printers:
            options.append(SelectOption(label=f"{printer.name} ({printer.model})", value=printer.id))
        return options

    def get_printer_by_id(self, _id):
        if type(_id) is str:
            _id = int(_id)
        return self.printers[_id]

    def update_printer(self, printer: Printer):
        self.printers[printer.id] = printer

