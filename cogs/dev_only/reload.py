import os

import discord
from discord.ext import commands
from bot.main import NewCommand

from bot.main import Emoji

class Reload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='reload',
        cls=NewCommand,
        brief="Reload a Cog",
        description="To Reload a Python Cog into the Bot",
        help="""This command is used to Reload the existing Cogs into the Bot.
The Cog should be Pre-Loaded into the Bot.
The Cog should be a Python File Only. No other Languages Work.
The Cog should be in the Proper directory as set by the Developer.""",
        usage="<cog_name:str>",
        explained_usage=["**Cog Name:** The Name of the Python File to be Reloaded."],
        permissions=['Developer Only'],
        examples=[
            'reload eval',
            'reload help'
        ]
    )
    @commands.is_owner()
    async def _reload(self, ctx, cog_name:str):
        _found = False
        for folders in os.scandir("./cogs"):
            for files in os.listdir(f"./cogs/{folders.name}"):
                if files.endswith('.py') and files[:-3] == cog_name:
                    self.client.reload_extension(f"cogs.{folders.name}.{files[:-3]}")
                    _found = True
                    return await ctx.reply(f"{Emoji.greentick} Successfully Reoaded `{cog_name}.py`")
        
        if _found is False:
            return await ctx.reply(f"{Emoji.redcross} No file named `{cog_name}` Found")


def setup(client):
    client.add_cog(Reload(client))