import os

import discord
from discord.ext import commands
from bot.main import NewCommand

from bot.main import Emoji, reply

class Unload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='unload',
        cls=NewCommand,
        brief="Unload a Cog",
        description="To Unload a Python Cog from the Bot",
        help="""This command is used to Unload the existing Cogs from the Bot.
The Cog should be Pre-Loaded into the Bot.
The Cog should be a Python File Only. No other Languages Work.
The Cog should be in the Proper directory as set by the Developer.""",
        usage="<cog_name:str>",
        explained_usage=["**Cog Name:** The Name of the Python File to be Unloaded."],
        permissions=['Developer Only'],
        examples=[
            'unload eval',
            'unload help'
        ]
    )
    @commands.is_owner()
    async def _unload(self, ctx, cog_name:str):
        _found = False
        for folders in os.scandir("./cogs"):
            for files in os.listdir(f"./cogs/{folders.name}"):
                if files.endswith('.py') and files[:-3] == cog_name:
                    self.client.unload_extension(f"cogs.{folders.name}.{files[:-3]}")
                    _found = True
                    return await reply(self.client, ctx, f"{Emoji.greentick} Successfully Unloaded `{cog_name}.py`")
        
        if _found is False:
            return await reply(self.client, ctx, f"{Emoji.redcross} No file named `{cog_name}` Found")


def setup(client):
    client.add_cog(Unload(client))