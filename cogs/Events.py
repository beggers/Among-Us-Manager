import discord
from discord.ext import commands

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from objects import *

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    """
        EVENTS: on_ready
                on_reaction_add
    """


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="am.help"))
        print('Bot is ready.')


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #Make sure reaction isn't from bot
        if user == self.client.user:
            return

        reaction = str(reaction)

        #Make sure reaction is releated to the game
        if reaction != '☠' and reaction != '📢' and reaction != '🔇' and reaction != '⏮':
            return

        #Variables needed
        try:
            voiceChannel = user.voice.channel
        except:
            return

        member = user

        gamecommand = self.client.get_cog('GameCommands')

        #Dead reaction
        if reaction == '☠':
            await gamecommand.changeDead(member, voiceChannel)

        #Meeting reaction
        if reaction == '📢':
            await gamecommand.changeStage(member, voiceChannel, Stage.Meeting)

        #Mute reaction
        if reaction == '🔇':
            await gamecommand.changeStage(member, voiceChannel, Stage.Round)

        #Meeting reaction
        if reaction == '⏮':
            await gamecommand.changeStage(member, voiceChannel, Stage.Lobby)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        else:
            print(error)
            return

def setup(bot):
    bot.add_cog(Events(bot))
