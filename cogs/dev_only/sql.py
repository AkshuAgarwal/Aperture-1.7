import io
import contextlib
import textwrap
from traceback import format_exception
import datetime

import discord
from discord.ext import commands
from tabulate import tabulate

from bot.main import NewCommand, StringPaginator, Emoji

class SQL(commands.Cog):
    def __init__(self, client):
        self.client = client

    def clean_query(self, query:str) -> str:
        if query.startswith("```") and query.endswith("```"):
            return " ".join(query.split("\n")[1:])[:-3]
        
        return query

    def chunk_result(self, ctx, result):
        entries = []
        _temp_entries = [f"```\n{result[i:i+1950]}\n```" for i in range(0, len(result), 1950)]
        for index, entry in enumerate(_temp_entries, start=1):
            entries.append(f"{entry} Page No: `{index}/{len(_temp_entries)}`")
        return entries

    @commands.command(
        name='sql',
        cls=NewCommand,
        aliases=['psotgres'],
        brief="Execute an SQL Statement!",
        description="To Execute SQL Statement in the Bot's Database",
        help="""This command can execute a SQL statement (PostreSQL) into the Bot to get Bot Data and do several Operations for Bot and Data Management.
This is a **Developer Only** Command. Means, only the Bot owner can use this Command.""",
        usage="<query_type:str('fetch'/'execute')> <query:str>",
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

        async with self.client.pool.acquire() as conn:
            async with conn.transaction() as trans:
                if query_type == "fetch":
                    temp_list = []
                    try:
                        data = await conn.fetch(query)
                        if not data:
                            return await ctx.reply(f"Output: []")
                        for row in data:
                            temp_list.append(list(row.values()))
                        table = tabulate(temp_list, headers=list(data[0].keys()), showindex="always", tablefmt="psql")
                        chunk_list = self.chunk_result(ctx, table)
                        pager = StringPaginator(
                            pages=chunk_list, timeout=180
                        )
                        await pager.start(ctx)
                    except Exception as e:
                        return await ctx.reply(f"{Emoji.redcross} **Oops! Some Error Occured...**\n> Error: `{e}`")
                        # raise e
                elif query_type == "execute":
                    try:
                        resp = await conn.execute(query)
                        return await ctx.reply(f"> Output: `{resp}`")
                    except Exception as e:
                        return await ctx.reply(f"{Emoji.redcross} **Oops! Some Error Occured...**\n> Error: `{e}`")
                else:
                    return await ctx.reply(f"{Emoji.redcross} Invalid Query Type! Valid Types: `fetch`/`execute`")


def setup(client):
    client.add_cog(SQL(client))