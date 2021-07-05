from discord.ext import commands

from bot.main import NewCommand, Emoji

from art import text2art

class ASCIIArt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="ascii",
        cls=NewCommand,
        aliases=["asciiart"],
        brief="ASCII Art!",
        description="Converts the Text to ASCII Art",
        help="""This command is used to convert the Text to ASCII Art.
Max Length of Text can be x Letters.""",
        explained_usage=["**Text:** The Text to Convert to ASCII Art."],
        usage="<text:str>",
        examples=[
            "ascii Hello, how are you?",
            "asciiart Hey, I'm Aperture!"
        ]
    )
    @commands.cooldown(2, 10, type=commands.BucketType.member)
    async def _asciiart(self, ctx, *, text: str):
        if len(text) > 25:
            return await ctx.reply(f"{Emoji.redcross} Length of Text cannot be more than 25 Characters!")

        art = text2art(text)

        if len(art) > 1990:
            return await ctx.reply(f"Oops! ASCII Art crossed more than 2000 Words. Please try a smaller Text.")

        await ctx.reply(f"```\n{art}```")


def setup(client):
    client.add_cog(ASCIIArt(client))
