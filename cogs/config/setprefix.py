from typing import Optional

from discord.ext import commands

from bot.main import NewCommand, Emoji, reply

class SetPrefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="setprefix",
        cls=NewCommand,
        brief="Change my Prefix!",
        description="Changes the Bot's Prefix for the Server",
        help="""This command is used to change the Bot's Prefix for the Server.
Maximum Length of the Prefix can be `5`.
The Prefix cannot contain Spaces.
You can also choose whether you want the Prefix to be Case Insensitive, i.e., if the Prefix is `ap!` and case_insensitive is True, then Bot will also respond to `Ap!`/`aP!`/`AP!`.""",
        usage="<prefix:str> [case_insensitive:bool(true/t/false/f), default:true]",
        explained_usage=["**Prefix:** Prefix for the Bot to be set.", "**Case Insensitive:** Whether to Accept prefix regardless of it's Case (True/False) [Optional, default:True]"],
        permissions=["Administrator"],
        examples=[
            'setprefix ap!',
            'setprefix ! false',
            'setprefix .. t'
        ]
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.guild_only()
    async def _setprefix(self, ctx, prefix:str, case_insensitive: Optional[str]="true"):
        if len(prefix) > 5:
            return await ctx.reply(f"{Emoji.redcross} Length of Prefix cannot be greater than `5` characters!")
        
        if case_insensitive.lower() in ["true", "t"]:
            case = True
        elif case_insensitive.lower() in ["false", "f"]:
            case = False
        else:
            return await reply(self.client, ctx, f"{Emoji.redcross} `{case_insensitive}` is not a Valid Boolean Type Accepted by the Bot...\nChoose from `True/t` or `False/f`")

        async with self.client.pool.acquire() as conn:
            async with conn.transaction() as trans:
                await conn.execute("UPDATE guild_data SET prefix=$1, prefix_case_insensitive=$2 WHERE guild_id=$3;", prefix, case, ctx.guild.id)
                self.client.prefixes[ctx.guild.id] = [prefix, case]
                return await reply(self.client, ctx, f"{Emoji.greentick} Successfully Changed prefix for this Server to `{prefix}`!")


def setup(client):
    client.add_cog(SetPrefix(client))