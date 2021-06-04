import os

import discord
from discord.ext import commands
from bot.main import NewCommand

from bot.main import Emoji
from bot.main import Errors

class Load(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='load',
        cls=NewCommand,
        brief="Load a Cog",
        description="To Load a Python Cog into the Bot",
        help="""This command is used to Load the Cogs into the Bot.
The Cog should be a Python File Only. No other Languages Work.
The Cog should be in the Proper directory as set by the Developer.""",
        usage="`load` `<cog_name:str>`",
        explained_usage=["**Cog Name:** The Name of the Python File to be Loaded."],
        permissions=['Developer Only'],
        examples=[
            'load eval',
            'load help'
        ]
    )
    @commands.is_owner()
    async def _load(self, ctx, cog_name:str):
        _found = False
        for folders in os.scandir("./cogs"):
            for files in os.listdir(f"./cogs/{folders.name}"):
                if files.endswith('.py') and files[:-3] == cog_name:
                    self.client.load_extension(f"cogs.{folders.name}.{files[:-3]}")
                    _found = True
                    return await ctx.reply(f"{Emoji.greentick} Successfully Loaded `{cog_name}.py`")
        
        if _found is False:
            return await ctx.reply(f"{Emoji.redcross} No file named `{cog_name}` Found")

    @_load.error
    async def _load_error(self, ctx, error):
        _error = getattr(error, "original", error)
        error = Errors(ctx, _error)
        await error.response()

def setup(client):
    client.add_cog(Load(client))