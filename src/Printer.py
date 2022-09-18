from datetime import datetime, timedelta
from enum import Enum

import pytz as pytz


class PrinterStatus(Enum):
    READY = 0
    PRINTING = 1
    DOWN = 2

class Printer:

    name: str
    make: str
    model: str
    status: PrinterStatus

    def __init__(self, bot, _id, name, model, status: PrinterStatus, user=None, note=None):
        self.bot = bot
        self.id = _id
        self.name = name
        self.model = model
        self.status = status
        self.user_id = user
        self.note = note

    async def get_formatted_output(self):
        symbol = str(self.status.value).replace("0", "✅").replace("1", "🖨️").replace("2", "⛔")
        out = f"{symbol} {self.name:<12} | {self.model:<12}"
        # out = '{:^17} | {:^17}'.format(self.name, self.model)
        # out = f"|{self.name:^15}|"

        user = self.user_id
        if user is not None:
            user_temp = await self.bot.guild.fetch_member(int(user))
            user = user_temp.nick
            if user is None:
                user = user_temp.name
            out = f"{out} | {user:<12}"

        note = self.note
        if self.status == PrinterStatus.PRINTING:
            epoch = int(note)
            utc_native_time = datetime.utcfromtimestamp(epoch)
            cst = pytz.timezone('US/Central')
            utc_time = pytz.utc.localize(utc_native_time)
            cst_time = utc_time.astimezone(cst)
            note = cst_time.strftime("%a, %b %d @ %I:%M%p")
            note = f"ETA: {note:<15}"
            out = f"{out} | {note}"
        elif note is not None:
            out = f"{out} | {note}"

        # print(out)
        return f"{out}"

    def cancel_print(self):
        self.status = PrinterStatus.READY
        self.user_id = None
        self.note = None

    def start_print(self, user, hours):
        self.status = PrinterStatus.PRINTING
        self.user_id = user.id
        note = (datetime.now() + timedelta(minutes=hours * 60)).timestamp()
        self.note = f"{note}".split(".")[0]

    def mark_problem(self, user, note):
        self.status = PrinterStatus.DOWN
        self.user_id = user.id
        self.note = note

    def mark_fixed(self):
        self.cancel_print()
        pass

    def __str__(self):
        user_id = self.user_id
        if user_id is None:
            user_id = ""

        note = self.note
        if note is None:
            note = ""

        return f"{self.id}|{self.name}|{self.model}|{self.status.value}|{user_id}|{note}"

def get_printer_from_database(line: str, bot):
    # print(f"GOT LINE: {line}")
    split = line.split("|")
    _id = int(split[0])
    name = split[1]
    model = split[2]
    status: PrinterStatus = PrinterStatus(int(split[3]))
    user = None
    note = None

    if status is not PrinterStatus.READY:
        if split[4] != "":
            user = int(split[4])
        if split[5] != "":
            note = split[5]

    return Printer(bot, _id, name, model, status, user, note)