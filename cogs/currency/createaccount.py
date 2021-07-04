from discord.ext import commands

from bot.main import NewCommand, reply, Emoji

class CreateAccount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='createaccount',
        cls=NewCommand,
        brief="Wanna Open a New Account?",
        description="Create an Apertures Currency Account!",
        help="""This command is used to Create an Account for the Apertures Currency!
The Bot has many Games and Features which requires you to have an Apertures Currency Account Registered in the Bot.
You can enjoy Bot Games, earn Apertures by Playing Games and many more!!!""",
        examples=[
            'createaccount'
        ]
    )
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def _createaccount(self, ctx):
        async with self.client.pool.acquire() as conn:
            async with conn.transaction() as trans:
                data = await conn.fetchrow('SELECT * FROM apertures_currency WHERE user_id=$1;', ctx.author.id)
                if not data:
                    await conn.execute('INSERT INTO apertures_currency (user_id, balance) VALUES ($1, 500);', ctx.author.id)
                    return await reply(self.client, ctx, f"{Emoji.greentick} Your Account has been Successfully Created with ID: `{ctx.author.id}`!\nYou can now enjoy playing different Games and earn Apertures too.")
                else:
                    return await reply(self.client, ctx, f"{Emoji.redcross} You already have an Account Registered!\n\n> **Tip:** To check your current Account Balance, use `{ctx.prefix}balance`!")


def setup(client):
    client.add_cog(CreateAccount(client))