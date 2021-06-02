import discord
from discord.ext import commands

from bot.main import NewCommand, Emoji, Errors

class ChannelManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="disablechannel",
        cls=NewCommand,
        brief="Disable me from a Channel",
        description="Disables the Bot to be operated in a Particular Channel",
        help="""This command is used to Disable the Bot to be operated/used in a Particular Channel in the Server.
All the Commands of the Bot cannot be used in that Channel but still be operatable in other Enabled Channels.""",
        usage="`disablechannel` `<channel:(id/mention)>`",
        explained_usage=["**Channel:** The Channel in which you want the Bot to be Disabled."],
        permissions=["Administrator"],
        cooldown="`1`/`10 sec` - [`Guild`]",
        examples=[
            'disablechannel #general',
            'disablechannel 844974705376881268'
        ]
    )
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def _disablechannel(self, ctx, channel:discord.TextChannel):
        async with self.client.pool.acquire() as conn:
            async with conn.transaction() as trans:
                data = await conn.fetch("SELECT * FROM guild_disabled WHERE guild_id=$1 AND channel_id=$2;", ctx.guild.id, channel.id)
                if not data:
                    await conn.execute("INSERT INTO guild_disabled (guild_id, channel_id) VALUES ($1, $2);", ctx.guild.id, channel.id)
                    return await ctx.reply(f"{Emoji.greentick} Successfully Disabled {channel.mention}")
                else:
                    return await ctx.reply(f"{Emoji.redcross} The Channel {channel.mention} is already Disabled")

    @_disablechannel.error
    async def _disablechannel_error(self, ctx, error):
        _error = getattr(error, "original", error)
        error = Errors(ctx, _error)
        resp = error.response()
        await ctx.reply(resp)

    @commands.command(
        name="enablechannel",
        cls=NewCommand,
        brief="Enable me in a Channel",
        description="Enables the Bot to be operated in a Particular Channel",
        help="""This command is used to Enable the Bot to be operated/used in a Particular Channel in the Server.
Only works if the Bot was already Disabled in that Channel.""",
        usage="`enablechannel` `<channel:(id/mention)>`",
        explained_usage=["**Channel:** The Channel in which you want the Bot to be Disabled."],
        permissions=["Administrator"],
        cooldown="`1`/`10 sec` - [`Guild`]",
        examples=[
            'enablechannel #general',
            'enablechannel 844974705376881268'
        ]
    )
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def _enablechannel(self, ctx, channel:discord.TextChannel):
        async with self.client.pool.acquire() as conn:
            async with conn.transaction() as trans:
                data = await conn.fetch("SELECT * FROM guild_disabled WHERE guild_id=$1 AND channel_id=$2;", ctx.guild.id, channel.id)
                if not data:
                    return await ctx.reply(f"{Emoji.redcross} The Channel {channel.mention} is already Enabled")
                else:
                    await conn.execute("DELETE FROM guild_disabled WHERE guild_id=$1 AND channel_id=$2;", ctx.guild.id, channel.id)
                    return await ctx.reply(f"{Emoji.greentick} Successfully Enabled {channel.mention}")

    @_enablechannel.error
    async def _enablechannel_error(self, ctx, error):
        _error = getattr(error, "original", error)
        error = Errors(ctx, _error)
        resp = error.response()
        await ctx.reply(resp)

def setup(client):
    client.add_cog(ChannelManagement(client))