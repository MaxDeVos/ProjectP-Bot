import discord


class EmojiVoter:
    def __init__(self, embed, channel: discord.TextChannel):
        self.embed = embed
        self.embed.title = "Emoji Vote | 4 posreps required"
        self.channel = channel

    def sendMessage(self):
        pass