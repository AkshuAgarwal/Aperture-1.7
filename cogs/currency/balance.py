from typing import Union
from datetime import datetime

from discord import User, Member, Embed
from discord.ext import commands

from bot.main import NewCommand, Emoji

class Balance(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='balance',
        cls=NewCommand,
        aliases=['bal'],
        brief="What's your Account Balance? :smirk:",
        description='Check your Apertures Account Balance',
        help="""This command is used to check your/any other user's Apertures Account current Balance.
You should have an Apertures Account Created to use this command.
Use `createaccount` to Create an Account or use `currencyinfo` to know more!""",
        usage='[user:name/id/@mention, default:command_invoker]',
        explained_usage=["**User:** User whose Balance you need to know. Can be Name, ID or Mention."],
        examples=[
            'balance',
            'balance @Akshu',
            'balance 764462046032560128',
            'balance Akshu#7472'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _balance(self, ctx, user:Union[User, Member]=None):
        if not user:
            user = ctx.author

        async with self.client.pool.acquire() as conn:
            data = await conn.fetchrow('SELECT balance FROM apertures_currency WHERE user_id=$1;', user.id)

            if not data:
                if user == ctx.author:
                    return await ctx.reply(f"{Emoji.redcross} You need to have an Apertures Currency Account first to check Balance or use commands that involves use of Bot Currency!\n\n> Use `{ctx.prefix}createaccount` to Create an Account and get Started.")
                else:
                    return await ctx.reply(f"{Emoji.redcross} {user} has no Apertures Currency Account Registered!\n\n> **Tip:** They can create an account using `{ctx.prefix}createaccount`.")
            else:
                embed = Embed(
                    title=f"{user}'s Balance",
                    description=f"> **{data['balance']} Apertures**",
                    color=0x00eeff,
                    timestamp=datetime.utcnow()
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f'Thanks for using {ctx.guild.me.name}', icon_url=ctx.guild.me.avatar_url)

                await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Balance(client))