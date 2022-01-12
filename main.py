import time

import discord

from EmojiHandler import EmojiHandler
from PinHandler import PinHandler
from RoleHandler import RoleHandler
import DataLogger
import LinkShortener
from HistoryManager import HistoryManager
import Voting
import LanguageHandler

# TODO role manager
# TODO cancel emoji votes after 4 days
# ---------------- History Manager ---------------------
# TODO give HistoryManager its own thread to avoid blocking responses while parsing server data
# TODO automatically collect and report emoji usage on the 1st day of every month
# TODO automatically update "chopping block" based on emoji usage data


f = open("data/key.txt", "r")
key = f.read()

# g = open("data/guild.max", "r")
# active_guild = int(g.read())

# Dangerous Men
active_guild = 375753471812435968

# Test Server
# noinspection PyRedeclaration
# active_guild = 782870393517768704


def getTimeStamp(stamp):
    return "[" + stamp + "] [" + time.strftime('%Y-%m-%d %H:%M:%S') + "]"


class Client(discord.Client):

    guild: discord.Guild

    def __init__(self):
        super().__init__()
        self.announcements_channel = None
        self.guild = None
        self.pinHandler = None
        self.roleHandler = None
        self.emojiHandler = None
        self.admin_channel = None
        self.roles_channel = None
        self.ant_zone = None
        self.fuck = None
        self.misc = None
        self.database = None

    async def on_ready(self):

        # self.database = MySQLHandler()

        await self.change_presence(activity=discord.Activity(name='Eat The Rich', type=discord.ActivityType.playing))
        for n in self.guilds:
            # if n.id ==
            if n.id == active_guild:
                self.guild = n
                print(getTimeStamp("SERVER"), "Found GUILD: " + self.guild.name)

        for a in self.guild.text_channels:

            if a.name == "emoji-voting":
                self.announcements_channel = a
                print(getTimeStamp("SERVER"), "Found Announcements Channel: ", str(self.announcements_channel.id))
                self.emojiHandler = EmojiHandler(self.guild, self.announcements_channel, self)

            # MISC
            if a.name == "nsfw":
                self.misc = a
                print(getTimeStamp("SERVER"), "Found Misc Channel: ", str(self.misc.id))

            if a.name == "pins":
                print(getTimeStamp("SERVER"), "Found Pins Channel")
                self.pinHandler = PinHandler(a, self.guild)

            if a.name == "admin-chat":
                print(getTimeStamp("SERVER"), "Found Admin Channel")
                self.admin_channel = a

            if a.name == "roles":
                print(getTimeStamp("SERVER"), "Found Roles Channel")
                self.roles_channel = a

            if a.name == "emotions-and-serious-stuff":
                print(getTimeStamp("SERVER"), "Found Ant Zone Channel")
                self.ant_zone = a

            if a.name == "server-announcements":
                self.fuck = a

        # self.emojiHandler.addVoters(await Voting.create_archived_votes(self))
        # self.roleHandler = RoleHandler(self.guild, self.admin_channel, self.roles_channel)

        # m = await self.misc.fetch_message(875120875622518804)
        # await m.reply("ahem")

        # Emergency Manual Pin - Channel ID Entry
        # c = await self.guild.fetch_channel(375804979564380171)
        # mes = await c.fetch_message(918005290543243345)
        # await self.pinHandler.pin(mes)

        # Emergency Manual Pin - MISC Entry
        # mes = await self.misc.fetch_message(914314438570569789)
        # await self.pinHandler.pin(mes)

        # Manual Pin Total Manual Entry
        # ch = await self.guild.fetch_channel(811872434378244106)
        # await ch.send("https://discord.com/channels/375753471812435968/663584506892124164/914314438570569789\n**Author:** <@155102908281520129>  |  **Channel:** <#663584506892124164>\nMESSAGE")

        # history = HistoryManager(self.guild, self.database)
        # await history.analyze_history()

    async def on_message(self, message: discord.Message):
        if message.guild.id == active_guild and not message.author.bot:
            # await LinkShortener.shorten_link(message)
            await LanguageHandler.determine_language(message)
            if self.emojiHandler is not None:
                await self.emojiHandler.handleEmojiMessage(message)
            if str(message.content).startswith("!role") and message.channel.id == self.admin_channel.id and not message.author.bot:
                self.roleHandler.handle_new_role(message)

    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):
        if reaction.guild_id == active_guild:
            await self.pinHandler.handlePinReaction(reaction, self)
            if self.emojiHandler is not None:
                await self.emojiHandler.handleEmojiVoters(reaction)

    # async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        # await self.database.addReaction(reaction)

    async def send_message(self, channel_name, message):
        channels = await self.guild.fetch_channels()
        for channel in channels:
            if channel.name == channel_name:
                await channel.send(message)

    # noinspection PyMethodMayBeStatic
    async def on_voice_state_update(self, user, old, new):
        DataLogger.handle_voice_state_change(user, old, new)

    async def join_vc(self, channel_name):
        channels = await self.guild.fetch_channels()
        for channel in channels:
            if channel.name == channel_name:
                await channel.connect()

    async def get_members(self):
        out = "["
        bruh = await self.guild.fetch_members()
        member: discord.Member
        for member in bruh:
            out += member.display_name + ","
        return bruh + "]"


client = Client()
client.run(key)
print("Successfully started bot")
