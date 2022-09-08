from src import Printer

async def load_printers(database_content, bot):
    out = []
    printers = await database_content
    for line in printers.split("\n"):
        out.append(Printer.get_printer_from_database(line, bot))
    return out

class PrinterManager:

    def __init__(self, bot, generate_status_message=False):
        self.status_message_id = None
        self.bot = bot
        self.printers = {}

    async def load_printers(self, database_content):
        self.printers = {}
        for printer in await load_printers(database_content, self.bot):
            self.printers[printer.id] = printer
            # print(printer)

    async def get_formatted_message(self):
        out = ""
        for printer in self.printers.values():
            formatted_line = await printer.get_formatted_output()
            out = f"{out}{formatted_line}\n"
        return out

    def get_database_message(self):
        out = ""
        for printer in self.printers.values():
            out = f"{out}{str(printer)}\n"
        return out
