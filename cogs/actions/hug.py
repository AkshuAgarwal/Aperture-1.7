from random import choice
from typing import Union
from datetime import datetime

from discord import User, Member, Embed
from discord.ext import commands

from bot.main import NewCommand, reply, Errors

class Hug(commands.Cog):
    def __init__(self, client):
        self.client = client

    def randomise(self, users:list):
        messages = [
            f'{users[0]} hugs {users[1]}!',
            f'{users[0]} gives {users[1]} a big hug!',
            f'{users[0]} gives a huge hug to {users[1]}!',
        ]
        gifs = [
            'https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif',
            'https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif',
            'https://media.giphy.com/media/GMFUrC8E8aWoo/giphy.gif',
            'https://media.giphy.com/media/svXXBgduBsJ1u/giphy.gif',
            'https://media.giphy.com/media/QFPoctlgZ5s0E/giphy.gif',
            'https://media.giphy.com/media/3bqtLDeiDtwhq/giphy.gif',
            'https://media.giphy.com/media/sUIZWMnfd4Mb6/giphy.gif',
            'https://media.giphy.com/media/lrr9rHuoJOE0w/giphy.gif',
            'https://media.giphy.com/media/du8yT5dStTeMg/giphy.gif',
            'https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif',
            'https://media.giphy.com/media/DjczAlIcyK1Co/giphy.gif',
            'https://media.giphy.com/media/2A75Y6NodD38I/giphy.gif',
            'https://media.giphy.com/media/10BcGXjbHOctZC/giphy.gif',
        ]

        return (choice(gifs), choice(messages))

    @commands.command(
        name='hug',
        cls=NewCommand,
        brief='A Hug for you!',
        description='Give someone a Tight Hug!',
        usage='`hug` `<user:name/id/@mention>`',
        explained_usage=["**User:** The User whom you wanna give a Hug!"],
        cooldown='`1/5 sec` - [`Member`]',
        examples=[
            'hug @Akshu',
            'hug 764462046032560128',
            'hug Akshu#7472'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def _hug(self, ctx, user:Union[User, Member]):
        gif, msg = self.randomise([ctx.author.name, user.name])

        embed=Embed(color=0x00eeff, timestamp=datetime.utcnow())
        embed.set_author(name=msg, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Thanks for using {ctx.guild.me.name}', icon_url=ctx.guild.me.avatar_url)
        embed.set_image(url=gif)
        await reply(self.client, ctx, embed=embed)

    @_hug.error
    async def _hug_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, error)
        await error.response()

def setup(client):
    client.add_cog(Hug(client))