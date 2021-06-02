import io
import contextlib
import textwrap
from traceback import format_exception
import datetime

import discord
from discord.ext import commands

from bot.main import NewCommand, Paginator, Errors, Emoji

class SQL(commands.Cog):
    def __init__(self, client):
        self.client = client

    def clean_query(self, query:str) -> str:
        if query.startswith("```") and query.endswith("```"):
            return " ".join(query.split("\n")[1:])[:-3]
        
        return query

    def make_embeds(self, ctx, result) -> list:
        embeds = []
        entries = [result[i:i+2000] for i in range(0, len(result), 2000)]
        for entry in entries:
            embed = discord.Embed(
                title='Output for SQL Query',
                description=f"```py\n{entry}```",
                color=0x2c2f33,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Page No. {entries.index(entry)+1}/{len(entries)}", icon_url=ctx.guild.me.avatar_url)
            embeds.append(embed)
        
        return embeds

    @commands.command(
        name='sql',
        cls=NewCommand,
        aliases=['psotgres'],
        brief="Execute an SQL Statement!",
        description="To Execute SQL Statement in the Bot's Database",
        help="""This command can execute a SQL statement (PostreSQL) into the Bot to get Bot Data and do several Operations for Bot and Data Management.
This is a **Developer Only** Command. Means, only the Bot owner can use this Command.""",
        usage="`sql` `<query_type:str(fetch/execute)>` `<query:str>`",
        explained_usage=["**Query Type:** Type of Query to Execute (`fetch`/`execute`)", "**Query:** The SQL Query to execute. Code blocks are also Accepted."],
        permissions=['Developer Only'],
        bot_permissions=['Manage Messages'],
        examples=[
            "sql execute INSERT INTO mytable VALUES (1, 'test');",
            'sql fetch ```sql\nSELECT * from table;```'
        ]
    )
    @commands.is_owner()
    async def _sql(self, ctx, query_type:str, *, query:str):
        query = self.clean_query(query)

        local_variables = {
            "_client": self.client
        }

        stdout = io.StringIO()

        if query_type == "fetch":
            code = f'''
async with _client.pool.acquire() as conn:
    async with conn.transaction() as trans:
        data = await conn.fetch('{query}')
        print(data)'''
        elif query_type == "execute":
            code = f'''
async with _client.pool.acquire() as conn:
    async with conn.transaction() as trans:
        await conn.execute('{query}')'''
        else:
            return await ctx.reply(f"{Emoji.redcross} Invalid Query Type! Valid Types: `fetch`/`execute`")

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
            pages = self.make_embeds(ctx, result),
            timeout=150
        )
        await pager.start(ctx)

    @_sql.error
    async def _sql_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, _error)
        resp = error.response()
        await ctx.reply(resp)

def setup(client):
    client.add_cog(SQL(client))