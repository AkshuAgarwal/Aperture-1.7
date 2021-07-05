import asyncio
import asyncpg
from discord.ext import commands
from discord import Message

from bot.main import Emoji

async def is_disabled(client, ctx: commands.Context):
    if not ctx.guild:
        return True
    else:
        try:
            guild_data = client.disabled_data[ctx.guild.id]
        except KeyError:
            async with client.pool.acquire() as conn:
                async with conn.transaction() as trans:
                    data = await conn.fetch("SELECT * FROM guild_disabled;")
                    for row in data:
                        client.disabled_data[row['guild_id']] = {
                            'channel_id': row['channel_id'],
                            'command_name': row['command_name']
                        }
                    try:
                        guild_data = client.disabled_data[ctx.guild.id]
                    except KeyError:
                        await conn.execute("INSERT INTO guild_disabled (guild_id, command_name, channel_id) VALUES ($1, array[]::varchar(30)[], array[]::bigint[]);", ctx.guild.id)
                        guild_data = client.disabled_data[ctx.guild.id] = {'channel_id': [], 'command_name': []}

        if not guild_data['channel_id']:
            channel_disabled = False
        elif ctx.channel.id not in guild_data['channel_id']:
            channel_disabled = False
        elif ctx.channel.id in guild_data['channel_id']:
            channel_disabled = True

        if not guild_data['command_name']:
            command_disabled = False
        elif ctx.command.name not in guild_data['command_name']:
            command_disabled = False
        elif ctx.command.name in guild_data['command_name']:
            command_disabled = True

        if command_disabled is True:
            await ctx.reply(f"{Emoji.redcross} The command is Disabled in this Server.")
            return False
        elif channel_disabled is True:
            await ctx.reply(f"{Emoji.redcross} The Bot is Disabled in this Channel. Try it in any another Channel.")
            return False
        else:
            return True