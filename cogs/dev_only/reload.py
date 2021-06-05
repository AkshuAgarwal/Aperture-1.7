import os

import discord
from discord.ext import commands
from bot.main import NewCommand

from bot.main import Emoji
from bot.main import Errors

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
        usage="`reload` `<cog_name:str>`",
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
                    try:
                        response = self.client.old_responses[ctx.message.id]
                        return await response.edit(content=f"{Emoji.greentick} Successfully Reoaded `{cog_name}.py`", embed=None, file=None, files=None, delete_after=None, allowed_mentions=None)
                    except KeyError:
                        response = await ctx.reply(f"{Emoji.greentick} Successfully Reoaded `{cog_name}.py`")
                        self.client.old_responses[ctx.message.id] = response
                        return
        
        if _found is False:
            try:
                response = self.client.old_responses[ctx.message.id]
                return await response.edit(content=f"{Emoji.redcross} No file named `{cog_name}` Found", embed=None, file=None, files=None, delete_after=None, allowed_mentions=None)
            except KeyError:
                response = await ctx.reply(f"{Emoji.redcross} No file named `{cog_name}` Found")
                self.client.old_responses[ctx.message.id] = response
                return

    @_reload.error
    async def _reload_error(self, ctx, error):
        _error = getattr(error, "original", error)
        error = Errors(ctx, _error)
        await error.response()

def setup(client):
    client.add_cog(Reload(client))