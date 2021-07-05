from discord.ext import commands

from bot.main import NewCommand

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
        examples=[
            'ping'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _ping(self, ctx):
        await ctx.reply(f":ping_pong: Pong! Latency: `{self.client.latency*1000:,.0f} ms`")


def setup(client):
    client.add_cog(Ping(client))