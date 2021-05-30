import asyncio
import asyncpg
from discord.ext import commands

async def is_disabled(client, ctx):
    async with client.pool.acquire() as conn:
        async with conn.transaction() as trans:
            data = await conn.fetch('SELECT * FROM guild_disabled WHERE guild_id=$1;', ctx.guild.id)
            if data:
                command_disabled, channel_disabled = False, False
                for entry in data:
                    if entry['command_name'] == ctx.command.name:
                        command_disabled = True
                    else:
                        if entry['channel_id'] == ctx.channel.id:
                            channel_disabled = True
                if command_disabled is True:
                    await ctx.reply("The command is disabled in this Server.")
                    return False
                elif channel_disabled is True:
                    await ctx.reply("The command is disabled in this Channel. Try it in any another Channel.")
                    return False
                else:
                    return True
            else:
                return True