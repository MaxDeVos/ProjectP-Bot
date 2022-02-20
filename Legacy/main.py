import time

import discord

from Legacy.EmojiHandler import EmojiHandler
from PinHandler import PinHandler
import DataLogger
import LanguageHandler

# TODO role manager
# TODO cancel emoji votes after 4 days
# ---------------- History Manager ---------------------
# TODO give HistoryManager its own thread to avoid blocking responses while parsing server data
# TODO automatically collect and report emoji usage on the 1st day of every month

f = open("data/test_key.txt", "r")
# f = open("data/key.txt", "r")
key = f.read()

# g = open("data/guild.max", "r")
# active_guild = int(g.read())

# Dangerous Men
# active_guild = 375753471812435968

# Test Server
# noinspection PyRedeclaration
active_guild = 782870393517768704


def getTimeStamp(stamp):
    return "[" + stamp + "] [" + time.strftime('%Y-%m-%d %H:%M:%S') + "]"


class Client(discord.Bot):

    guild: discord.Guild

    def __init__(self):
        super().__init__("/")
        self.channelDict = {}
        self.announcements_channel = None
        self.guild = None
        self.pinHandler = None
        self.roleHandler = None
        self.emojiHandler = None
        self.emergencyMention = None
        self.emergencyResponderMessageID = None

    async def on_ready(self):

        await self.change_presence(activity=discord.Activity(name='Eat The Rich', type=discord.ActivityType.playing))

        for n in self.guilds:
            if n.id == active_guild:
                self.guild = n
                print(getTimeStamp("SERVER"), "Found GUILD: " + self.guild.name)

        for a in self.guild.text_channels:
            self.channelDict[a.name] = a

        for role in await self.guild.fetch_roles():
            if role.name == "Emergency":
                self.emergencyMention = role.mention

        emKeyReader = open("data/emergencyResponderMessageID.max", "r")
        self.emergencyResponderMessageID = int(emKeyReader.read())
        print(self.emergencyResponderMessageID)

        self.pinHandler = PinHandler(self.channelDict["pins"], self.guild)
        print(getTimeStamp("PINS"), "Starting Pin Manager")

        self.emojiHandler = EmojiHandler(self.guild, self.channelDict["emoji-voting"], self)
        print(getTimeStamp("SERVER"), "Started Emoji Voter")

        # self.emojiHandler.addVoters(await Voting.create_archived_votes(self))
        # self.roleHandler = RoleHandler(self.guild, self.admin_channel, self.roles_channel)

        # Emergency Manual Pin - Channel ID Entry
        # c = await self.guild.fetch_channel(375804979564380171)
        # mes = await c.fetch_message(923809486622318592)
        # await self.pinHandler.pin(mes, True)

        # Emergency Manual Pin - Channel + Thread ID Entry
        # c = await self.guild.fetch_channel(375804979564380171)
        # c = c.get_thread(874745495619272724)
        # mes = await c.fetch_message(923809486622318592)
        # await self.pinHandler.pin(mes, True)

        # Emergency Manual Pin - MISC Entry
        # mes = await self.channelDict["general"].fetch_message(917194033695178762)
        # await self.pinHandler.pin(mes, True)

        # Manual Message
        # ch = await self.guild.fetch_channel(813312781906346024)
        # await ch.send("TEST")

        # Manual Reply
        # m = await self.misc.fetch_message(875120875622518804)
        # await m.reply("ahem")

        # history = HistoryManager(self.guild, self.database)
        # await history.analyze_history()

    async def on_message(self, message: discord.Message):
        if message.guild.id == active_guild and not message.author.bot:
            await LanguageHandler.determine_language(message)
            if self.emojiHandler is not None:
                await self.emojiHandler.handleEmojiMessage(message)
            if str(message.content).startswith(
                    "!role") and message.channel.id == self.channelDict["admin-chat"].id and not message.author.bot:
                self.roleHandler.handle_new_role(message)

    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):
        if reaction.message_id == self.emergencyResponderMessageID and not reaction.member.bot:
            await reaction.member.add_roles(self.guild.get_role(941400388786061402))
            print("Gave Emergency to " + reaction.member.display_name)
        if reaction.guild_id == active_guild:
            await self.pinHandler.handlePinReaction(reaction, self)
            if self.emojiHandler is not None:
                await self.emojiHandler.handleEmojiVoters(reaction)

    async def on_raw_reaction_remove(self, reaction: discord.RawReactionActionEvent):
        if reaction.message_id == self.emergencyResponderMessageID:
            mem = await self.guild.fetch_member(reaction.user_id)
            await mem.remove_roles(self.guild.get_role(941400388786061402))

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

@client.slash_command(guild_ids=[782870393517768704])
async def testt(ctx):
    await ctx.respond("I did something")

client.run(key)
