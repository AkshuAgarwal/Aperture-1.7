from random import choice
from typing import Union
from datetime import datetime

from discord import User, Member, Embed
from discord.ext import commands

from bot.main import NewCommand, reply

class Kiss(commands.Cog):
    def __init__(self, client):
        self.client = client

    def randomise(self, users:list):
        messages = [
            f'{users[0]} kissed {users[1]}!',
            f'{users[0]} gives {users[1]} a Kiss!',
            f'{users[0]} kissed {users[1]}! Adorable',
            f'{users[0]} kissed {users[1]}! How Cute!!'
        ]
        gifs = [
            'https://media.giphy.com/media/bGm9FuBCGg4SY/giphy.gif',
            'https://media.giphy.com/media/bm2O3nXTcKJeU/giphy.gif',
            'https://media.giphy.com/media/zkppEMFvRX5FC/giphy.gif',
            'https://media.giphy.com/media/nyGFcsP0kAobm/giphy.gif,'
            'https://media.giphy.com/media/vUrwEOLtBUnJe/giphy.gif',
            'https://media.giphy.com/media/IdzovcoOUoUM0/giphy.gif',
            'https://media.giphy.com/media/12VXIxKaIEarL2/giphy.gif',
            'https://media.giphy.com/media/ONq87vZz4626k/giphy.gif',
            'https://media.giphy.com/media/QGc8RgRvMonFm/giphy.gif',
            'https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif',
            'https://media.giphy.com/media/flmwfIpFVrSKI/giphy.gif'
        ]

        return (choice(gifs), choice(messages))

    @commands.command(
        name='kiss',
        cls=NewCommand,
        brief='Kiss Me!',
        description='Kiss someone with a Cute Gif!',
        usage='<user:name/id/@mention>',
        explained_usage=["**User:** The User whom you wanna give a Kiss!"],
        examples=[
            'kiss @Akshu',
            'kiss 764462046032560128',
            'kiss Akshu#7472'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def _kiss(self, ctx, user:Union[User, Member]):
        gif, msg = self.randomise([ctx.author.name, user.name])

        embed=Embed(color=0x00eeff, timestamp=datetime.utcnow())
        embed.set_author(name=msg, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Thanks for using {ctx.guild.me.name}', icon_url=ctx.guild.me.avatar_url)
        embed.set_image(url=gif)
        await reply(self.client, ctx, embed=embed)

def setup(client):
    client.add_cog(Kiss(client))