from discord.ext import commands

from bot.main import NewCommand, Errors

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="ping",
        aliases=["latency"],
        cls=NewCommand,
        brief=":ping_pong: Pong!",
        description="Get the Latency of the Bot",
        help="""This command is used to get the Latency of the Bot with Discord WebSocket.
More Scientifically, Measures Latency between a HEARTBEAT and HEARTBEAT_ACK in seconds.""",
        usage="`ping`",
        cooldown="`1/5 sec` - [`User`]",
        examples=[
            'ping'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _ping(self, ctx):
        try:
            response = self.client.old_responses[ctx.message.id]
            await response.edit(content=f":ping_pong: Pong! Latency: `{self.client.latency*1000:,.0f} ms`", embed=None, file=None, files=None, delete_after=None, allowed_mentions=None)
        except KeyError:
            response = await ctx.reply(f":ping_pong: Pong! Latency: `{self.client.latency*1000:,.0f} ms`")
            self.client.old_responses[ctx.message.id] = response
    
    @_ping.error
    async def _ping_error(self, ctx, error):
        _error = getattr(error, "original", error)
        error = Errors(ctx, _error)
        await error.response()

def setup(client):
    client.add_cog(Ping(client))