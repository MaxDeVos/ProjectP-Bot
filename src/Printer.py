from datetime import datetime
from enum import Enum

import discord
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
    note: str

    def __init__(self, bot, _id, name, model, status: PrinterStatus, user=None, note=None):
        self.bot = bot
        self.id = _id
        self.name = name
        self.model = model
        self.status = status
        self.user = user
        self.note = note

    async def get_formatted_output(self):
        symbol = str(self.status.value).replace("0", "✅").replace("1", "⌛").replace("2", "⛔")
        out = f"{symbol} {self.name} ({self.model})"

        user = self.user
        if user is not None:
            user_temp = await self.bot.fetch_user(int(user))
            user = user_temp.mention
            out = f"{out} | {user}"

        note = self.note
        if self.status == PrinterStatus.PRINTING:
            epoch = int(note)
            utc = datetime.utcfromtimestamp(epoch)
            timezone = pytz.timezone("America/Chicago")
            local_time = timezone.localize(utc)
            note = local_time.strftime("%a, %b %d @ %I:%M%p")
            note = f"ETA: {note}"

        out = f"{out} | {note}"
        print(out)
        return out

    def __str__(self):
        user = self.user
        if user is None:
            user = ""

        note = self.note
        if note is None:
            note = ""

        return f"{self.id}|{self.name}|{self.model}|{self.status.value}|{user}|{note}"

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