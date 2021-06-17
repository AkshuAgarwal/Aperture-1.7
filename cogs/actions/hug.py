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
            f'{users[0]} gives {users[1]} a big hug!'
        ]
        gifs = [
            'https://media1.tenor.com/images/a211f33e4ff688f9101a46ed95f2fb21/tenor.gif',
            'https://media1.tenor.com/images/4d89d7f963b41a416ec8a55230dab31b/tenor.gif',
            'https://media1.tenor.com/images/f5df55943b64922b6b16aa63d43243a6/tenor.gif',
            'https://media1.tenor.com/images/506aa95bbb0a71351bcaa753eaa2a45c/tenor.gif',
            'https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif',
            'https://media1.tenor.com/images/53c1172d85491e363ce58b20ba83cdab/tenor.gif'
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