from datetime import datetime
from typing import Union

from discord import Member, User, Embed
from discord.ext import commands

from bot.main import NewCommand, reply

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='avatar',
        cls=NewCommand,
        aliases=['av'],
        brief='That Avatar looks cool!',
        description='Get the Avatar of a User',
        help="""This command is used to get the Avatar of a User/Member.
The Member should be visible to Me. That means I need to share atleast 1 common Server with the user of whom I need to get the Avatar.""",
        usage='[user:name/id/@mention, default:command_invoker]',
        explained_usage=["**User:** User whose Avatar you need to get. Can be Name, ID or Mention."],
        examples=[
            'avatar',
            'avatar 764462046032560128',
            'avatar @Akshu'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def _avatar(self, ctx, user:Union[User, Member]=None):
        if not user:
            user = ctx.author
            
        if not user.avatar:
            desc = f"> **Download Avatar:**\n> [png]({user.avatar_url})"
        elif user.is_avatar_animated() is False:
            desc = f"> **Download Avatar:**\n> [webp]({user.avatar_url_as(format='webp')}) | [jpeg]({user.avatar_url_as(format='jpeg')}) | [jpg]({user.avatar_url_as(format='jpg')}) | [png]({user.avatar_url_as(format='png')})"
        elif user.is_avatar_animated() is True:
            desc = f"> **Download Avatar:**\n> [gif]({user.avatar_url_as(format='gif')}) | [webp]({user.avatar_url_as(format='webp')}) | [jpeg]({user.avatar_url_as(format='jpeg')}) | [jpg]({user.avatar_url_as(format='jpg')}) | [png]({user.avatar_url_as(format='png')})"

        embed = Embed(title=f"{user}'s Avatar", description=desc, color=0x00eeff, timestamp=datetime.utcnow())
        embed.set_author(name=user, icon_url=user.avatar_url)
        embed.set_footer(text=f'Thanks for using {ctx.guild.me.name}', icon_url=ctx.guild.me.avatar_url)
        embed.set_image(url=user.avatar_url)
        
        await reply(self.client, ctx, embed=embed)

def setup(client):
    client.add_cog(Avatar(client))