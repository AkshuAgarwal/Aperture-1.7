import asyncio
import datetime
from contextlib import suppress

import discord
from discord.ext import commands

from bot.main import NewCommand, Emoji

class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client

    def lte(self, key):
        myd = {
            1: ':one:',
            2: ':two:',
            3: ':three:',
            4: ':four:',
            5: ':five:',
            6: ':six:',
            7: ':seven:',
            8: ':eight:',
            9: ':nine:',
            'x': ':x:',
            'o': ':o:'
        }
        return myd[key]

    def etl(self, key):
        valid_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        ind = valid_emojis.index(key)
        return int(ind+1)


    def win(self, k: list):
        if k[0] == k[1] == k[2]:
            return (True, k[0])
        elif k[3] == k[4] == k[5]:
            return (True, k[3])
        elif k[6] == k[7] == k[8]:
            return (True, k[6])
        elif k[0] == k[3] == k[6]:
            return (True, k[0])
        elif k[1] == k[4] == k[7]:
            return (True, k[1])
        elif k[2] == k[5] == k[8]:
            return (True, k[2])
        elif k[0] == k[4] == k[8]:
            return (True, k[0])
        elif k[2] == k[4] == k[6]:
            return (True, k[2])
        else:
            return (False, 9)

    async def board(self, ctx, msg, players:list, keys:list, turn:list):
        gamestatus = discord.Embed(
            title=f"TicTacToe- {players[0]} vs {players[1]}",
            description=f"It's {turn[1].mention}'s ({self.lte(turn[0])}) Turn",
            color=0x00eeff,
            timestamp=datetime.datetime.utcnow()
        )
        gamestatus.set_footer(text=f"Thanks for using {ctx.guild.me.name}", icon_url=ctx.guild.me.avatar_url)
        gamestatus.set_author(name=f"{ctx.guild.me.name} Games", icon_url=ctx.guild.me.avatar_url)

        myboard = f"""{self.lte(keys[0])}{self.lte(keys[1])}{self.lte(keys[2])}
{self.lte(keys[3])}{self.lte(keys[4])}{self.lte(keys[5])}
{self.lte(keys[6])}{self.lte(keys[7])}{self.lte(keys[8])}"""
        await msg.edit(embed=gamestatus, content=myboard)

    async def start(self, ctx, response:discord.Message, players:list):
        l:list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        curturn = ['x', players[0]]
        state:bool = True
        x:int = 0
        await response.edit(content=f"{Emoji.loading} Creating the Board...")

        valid_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

        await self.board(ctx, response, players, l, curturn)
        for e in valid_emojis:
            await response.add_reaction(str(e))

        while state is True:
            (won, winner) = self.win(l)
            if won:
                if winner == 'x':
                    winner2 = players[0]
                elif winner == 'o':
                    winner2 = players[1]
                await response.clear_reactions()
                myboard = f"""{self.lte(l[0])}{self.lte(l[1])}{self.lte(l[2])}
{self.lte(l[3])}{self.lte(l[4])}{self.lte(l[5])}
{self.lte(l[6])}{self.lte(l[7])}{self.lte(l[8])}"""
                embed = discord.Embed(title=f"TicTacToe- {players[0]} vs {players[1]}",
                                    description=f":tada: {winner2.mention} ({self.lte(winner)}) Won!",
                                    color=0x00eeff, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"Thanks for using {ctx.guild.me.name}", icon_url=ctx.guild.me.avatar_url)
                embed.set_author(name=f"{ctx.guild.me.name} Games", icon_url=ctx.guild.me.avatar_url)
                return await response.edit(content=myboard, embed=embed)
            elif x == 9 and won is False:
                await response.clear_reactions()
                myboard = f"""{self.lte(l[0])}{self.lte(l[1])}{self.lte(l[2])}
{self.lte(l[3])}{self.lte(l[4])}{self.lte(l[5])}
{self.lte(l[6])}{self.lte(l[7])}{self.lte(l[8])}"""
                embed = discord.Embed(title=f"TicTacToe- {players[0]} vs {players[1]}",
                                    description=f"Match Draw!", color=0x00eeff, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"Thanks for using {ctx.guild.me.name}", icon_url=ctx.guild.me.avatar_url)
                embed.set_author(name=f"{ctx.guild.me.name} Games", icon_url=ctx.guild.me.avatar_url)
                return await response.edit(content=myboard, embed=embed)
            else:
                board = await self.board(ctx, response, players, l, curturn)

                if x % 2 == 0:
                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=180, check=lambda reaction, user: user.id == players[0].id and not user.bot and reaction.emoji in valid_emojis and reaction.message == response)
                        await response.clear_reaction(reaction.emoji)
                    except asyncio.exceptions.TimeoutError:
                        embed = discord.Embed(title=f"TicTacToe- {players[0]} vs {players[1]}",
                                            description=f"Timed Out Waiting for Response! Please Restart the Match...",
                                            color=0x00eeff, timestamp=datetime.datetime.utcnow())
                        embed.set_footer(text=f"Thanks for using {ctx.guild.me.name}", icon_url=ctx.guild.me.avatar_url)
                        embed.set_author(name=f"{ctx.guild.me.name} Games", icon_url=ctx.guild.me.avatar_url)
                        await response.clear_reactions()
                        return await response.edit(content="", embed=embed)
                    try:
                        ind = l.index(int(self.etl(reaction.emoji)))
                        l[ind] = 'x'
                        x += 1
                        curturn[0] = 'o'
                        curturn[1] = players[1]
                    except ValueError:
                        await ctx.send("This Position is not Available! Please try Another...", delete_after=10)
                elif x % 2 == 1:
                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=180, check=lambda reaction, user: user.id == players[1].id and not user.bot and reaction.emoji in valid_emojis and reaction.message == response)

                        await response.clear_reaction(reaction.emoji)
                    except asyncio.exceptions.TimeoutError:
                        embed = discord.Embed(title=f"TicTacToe- {players[0]} vs {players[1]}",
                                            description=f"Timed Out Waiting for Response! Please Restart the Match...",
                                            color=0x00eeff, timestamp=datetime.datetime.utcnow())
                        embed.set_footer(text=f"Thanks for using {ctx.guild.me.name}", icon_url=ctx.guild.me.avatar_url)
                        embed.set_author(name=f"{ctx.guild.me.name} Games", icon_url=ctx.guild.me.avatar_url)
                        await response.clear_reactions()
                        return await response.edit(content="", embed=embed)
                    try:
                        ind = l.index(int(self.etl(reaction.emoji)))
                        l[ind] = 'o'
                        x += 1
                        curturn[0] = 'x'
                        curturn[1] = players[0]
                    except ValueError:
                        await ctx.send("This Position is not Available! Please try Another...", delete_after=10)

    @commands.command(
        name="tictactoe",
        cls=NewCommand,
        aliases=['ttt'],
        brief="Let's have a Match of Tic-Tac-Toe!",
        description="Starts a Match of Tic-Tac-Toe Game",
        help="""This command is used to Start a game of Tic-Tac-Toe which can be played by 2 Players against Each Other.
In this Game, 2 players take turns marking the spaces in a 3×3 grid with the Symbols assigned to them (`X` and `O`).
The player who succeeds in placing three of their marks in a diagonal, horizontal, or vertical row is the winner.""",
        usage="`tictactoe`",
        bot_permissions=['Manage Messages'],
        cooldown="`1/15 sec` - [`User`]",
        examples=[
            'tictactoe'
        ]
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.guild_only()
    async def _tictactoe(self, ctx):
        players = [ctx.author]
        redcross = self.client.get_emoji(int((Emoji.redcross)[-19:-1]))
        greentick = self.client.get_emoji(int((Emoji.greentick)[-19:-1]))
        emojis = ['🚪', redcross, greentick]
        
        try:
            response = self.client.old_responses[ctx.message.id]
            await response.edit(content=f"**A Game of TicTacToe is going to be Started!**\nReact on this Message with {emojis[0]} to Enter or {emojis[1]} to Cancel.\n> Players Required: 2, Timeout: 3 Minutes\n\n> Participants: {ctx.author.mention}", embed=None, file=None, files=None, delete_after=None, allowed_mentions=None)
        except KeyError:
            response = await ctx.reply(f"**A Game of TicTacToe is going to be Started!**\nReact on this Message with {emojis[0]} to Enter or {emojis[1]} to Cancel.\n> Players Required: 2, Timeout: 3 Minutes\n\n> Participants: {ctx.author.mention}")
            self.client.old_responses[ctx.message.id] = response

        await response.add_reaction(emojis[0])
        await response.add_reaction(emojis[1])

        try:
            def maincheck(reaction, user):
                if reaction.message == response and not user.bot:
                    if reaction.emoji == emojis[0] and user not in players:
                        return True
                    elif reaction.emoji == emojis[1] and user == ctx.author:
                        return True
                    else:
                        return False
                else:
                    return False

            reaction, user = await self.client.wait_for('reaction_add', timeout=180, check=maincheck)
            
            if reaction.emoji == emojis[0]:
                players.append(user)
                await response.edit(content=f"**A Game of TicTacToe is going to be Started!**\n> Players Required: 2, Timeout: 3 Minutes\n\n> Participants: {ctx.author.mention}, {user.mention}.\nReact with {emojis[2]} to Start or {emojis[1]} to Cancel!")

                with suppress(Exception):
                    await response.clear_reactions()
                await response.add_reaction(emojis[2])
                await response.add_reaction(emojis[1])

                reaction, _ = await self.client.wait_for('reaction_add', timeout=180,
                                check=lambda reaction, user: reaction.emoji in [emojis[1], emojis[2]] and user == ctx.author and reaction.message == response)
                
                if reaction.emoji == emojis[2]:
                    await response.clear_reactions()
                    return await self.start(ctx, response, players)

                elif reaction.emoji == emojis[1]:
                    with suppress(Exception):
                        await response.clear_reactions()
                    return await response.edit(content=f"{Emoji.greentick} Cancelled the Match!")
            
            elif reaction.emoji == emojis[1]:
                with suppress(Exception):
                    await response.clear_reactions()
                return await response.edit(content=f"{Emoji.greentick} Cancelled the Match!")

        except asyncio.exceptions.TimeoutError:
            await response.clear_reactions()
            await response.edit(content="Timed out waiting for Players...")



def setup(client):
    client.add_cog(TicTacToe(client))