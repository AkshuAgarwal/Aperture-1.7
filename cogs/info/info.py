from datetime import datetime

from discord import Embed
from discord.ext import commands

from bot.main import NewCommand

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.info = None
        self.client.loop.create_task(self.get_info())

    async def get_info(self):
        self.info = await self.client.application_info()

    @commands.command(
        name='info',
        aliases=['about'],
        cls=NewCommand,
        brief='Who am I?',
        description='Shows some Information about me',
        help='''This command is used to know some basic Information about me.
This includes about me and my Developers.''',
        examples=[
            'info',
            'about'
        ]
    )
    @commands.bot_has_permissions(send_messages=True, emebd_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _info(self, ctx):
        info = self.client.application_info()
        embed = Embed(
            title=f'About {ctx.guild.me.name}',
            description="""I'm Aperture, a Multi-Puropse Discord Bot which can fulfill all your needs for maintaining a Discord Server in a single Bot!
I have a lot of various types of commands like Games, Info, Moderation, General and Currency... And more are on the way ;)
I'm made in Python with the help of discord.py API Wrapper.""",
            color=0x00eeff, timestamp=datetime.utcnow()
        ).set_author(
            name=ctx.author, icon_url=ctx.author.avatar_url
        ).set_footer(
            text=f'Thanks for using {ctx.guild.me.name}', icon_url=ctx.guild.me.avatar_url
        ).set_thumbnail(
            url=ctx.guild.me.avatar_url
        ).add_field(
            name='Developers', value=f'{self.info.owner} - {self.info.owner.id} [{self.info.owner.mention}]'
        )
        await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(Info(client))