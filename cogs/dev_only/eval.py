import io
import contextlib
import textwrap
from traceback import format_exception
import datetime

import discord
from discord.ext import commands

from bot.main import NewCommand, Paginator, Errors

class Eval(commands.Cog):
    def __init__(self, client):
        self.client = client

    def clean_code(self, code:str) -> str:
        if code.startswith("```") and code.endswith("```"):
            return "\n".join(code.split("\n")[1:])[:-3]

        return code

    def make_embeds(self, ctx, result) -> list:
        embeds = []
        entries = [result[i:i+2000] for i in range(0, len(result), 2000)]
        for entry in entries:
            embed = discord.Embed(
                title='Output for Python Eval Query',
                description=f"```py\n{entry}```",
                color=0x2c2f33,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Page No. {entries.index(entry)+1}/{len(entries)}", icon_url=ctx.guild.me.avatar_url)
            embeds.append(embed)
        
        return embeds

    @commands.command(
        name='eval',
        cls=NewCommand,
        aliases=['exec'],
        brief="Execute a Python Code!",
        description="To Execute Python Code in the Bot",
        help="""This command can execute a Python Script into the Bot to get Bot Data and do several Operations for Bot and Data Management.
This is a **Developer Only** Command. Means, only the Bot owner can use this Command.""",
        usage="`eval` `<code:str>`",
        explained_usage=["**Code:** The Python Code to execute. Code blocks are also Accepted."],
        permissions=['Developer Only'],
        bot_permissions=['Manage Messages'],
        examples=[
            'eval print("Hello, World!")',
            'eval ```py\na = 10```'
        ]
    )
    @commands.is_owner()
    async def _eval(self, ctx, *, code:str):
        code = self.clean_code(code)

        local_variables = {
            '_discord': discord,
            '_commands': commands,
            '_client': self.client,
            '_ctx': ctx,
            '_channel': ctx.channel,
            '_author': ctx.author,
            '_guild': ctx.guild,
            '_message': ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables
                )

                obj = await local_variables['func']()
                result = f"{stdout.getvalue()}\n-- {obj}\n"

        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = Paginator(
            pages=self.make_embeds(ctx, result),
            timeout=150
        )
        await pager.start(ctx)

    @_eval.error
    async def _eval_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, _error)
        await error.response()

def setup(client):
    client.add_cog(Eval(client))