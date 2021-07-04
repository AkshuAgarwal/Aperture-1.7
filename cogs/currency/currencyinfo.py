from datetime import datetime

from discord import Embed
from discord.ext import commands

from bot.main import NewCommand, reply

class CurrenccyInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='currencyinfo',
        cls=NewCommand,
        aliases=['aperturesinfo'],
        brief='Btw, what are Apertures?',
        description="Get info about Bot's Currency - Apertures",
        help="""This command is used to get all the info about the Bot's Currency, also known as Apertures!""",
        examples=[
            'currencyinfo'
        ]
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _currencyinfo(self, ctx):
        embed = Embed(
            title='Apertures Info',
            description=f"""\"Apertures\" is the Global Currency of the Aperture Bot.
The Currency can be used to play Bot Games like Tic-Tac-Toe and many more.

Users can compete in Games where they can Win Apertures, but can also Lose some ;)!
Most of the games in the Bot, and maybe some features too, requires you to have Currency to use them. So the more money you have, the more you can Enjoy with the Bot! Isn't that Cool!!

But how do I earn them?
That's simple! Just play Bot games and if you win, you will be Rewarded with Money. Note that if you lose, some Money will be Deducted from your Account too!

So what are you waiting for? Create an Account by using `{ctx.prefix}createaccount` and get Started!
""",
            color=0x00eeff,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Thanks for using {ctx.guild.me.name}', icon_url=ctx.guild.me.avatar_url)

        await reply(self.client, ctx, embed=embed)


def setup(client):
    client.add_cog(CurrenccyInfo(client))