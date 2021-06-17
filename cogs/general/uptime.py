from datetime import datetime

from discord.ext import commands

from bot.main import NewCommand, reply, Errors

class Uptime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="uptime",
        cls=NewCommand,
        brief=":clock: It's been long since I'm Working!",
        description="Get the Uptime of the Bot",
        help="""This command is used to get the Uptime of the Bot since it got Started.""",
        usage="`uptime`",
        cooldown="`1/5 sec` - [`User`]",
        examples=[
            'uptime'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _uptime(self, ctx: commands.Context):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        return await reply(self.client, ctx, f"I've been Up since {days} Days, {hours} Hours, {minutes} Minutes, and {seconds} Seconds!")

    @_uptime.error
    async def _uptime_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, _error)
        await error.response()

def setup(client):
    client.add_cog(Uptime(client))