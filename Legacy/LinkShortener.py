import discord
import re

async def shorten_link(message: discord.Message):

    latch = True

    if str(message.content).__contains__("https://"):
        links = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', message.content)
        for link in links:
            print(link)
            split = str.split(link, "?")
            new_link = split[0]
            num = (len(link) - len(new_link))
            dem = len(link)
            dif = (num / dem) * 100
            if dif > 45:
                if latch:
                    await message.reply(
                        "What kind of fucking link is that?  This link literally does the same thing and it's **" + str(
                            dif) + "%** shorter.  You absolute moron.\n" + new_link)
                    latch = False
                else:
                    await message.reply(
                        "This one too, dipshit.  It's **" + str(
                            dif) + "%** shorter.\n" + new_link)