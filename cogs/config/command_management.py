import discord
from discord.ext import commands

from bot.main import NewCommand, Emoji, Errors

class CommandManagement(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.non_disable_commands = [
            "help", "eval", "load", "unload", "reload", "disablecommand", "enablecommand"
        ]

    @commands.command(
        name="disablecommand",
        cls=NewCommand,
        brief="Disable a Command",
        description="Disables a Commmand for this Server",
        help="""This command is used to Disable any command of the Bot in the Server.
Some commands like Help, Developer and Configure Commands cannot be Disabled.
You can also use Command Alias instead of it's Name to Disable it.""",
        usage="`disablecommand` `<command_name:str>`",
        explained_usage=["**Command Name:** Name of the Command to be Disabled."],
        permissions=["Administrator"],
        cooldown="`1`/`10 sec` - [`Guild`]",
        examples=[
            'disablecommand ping',
            'disablecommand tictactoe'
        ]
    )
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def _disablecommand(self, ctx, command_name:str):
        command = discord.utils.find(lambda cmd: cmd.name == command_name or command_name in cmd.aliases, self.client.commands)
        if not command:
            return await ctx.reply(f"{Emoji.redcross} No Such Command Found")
        elif command.name in self.non_disable_commands:
            return await ctx.reply(f"{Emoji.redcross} This command cannot be Disabled!")
        else:
            async with self.client.pool.acquire() as conn:
                async with conn.transaction() as trans:
                    data = await conn.fetch("SELECT * FROM guild_disabled WHERE guild_id=$1 AND command_name=$2", ctx.guild.id, command.name)
                    if not data:
                        await conn.execute("INSERT INTO guild_disabled (guild_id, command_name) VALUES ($1, $2);", ctx.guild.id, command.name)
                        return await ctx.reply(f"{Emoji.greentick} Successfully Disabled Command `{command.name}` for this Server")
                    else:
                        return await ctx.reply("This command is Already Disabled in this Server")

    @_disablecommand.error
    async def _disablecommand_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, _error)
        resp = error.response()
        await ctx.reply(resp)

    @commands.command(
        name="enablecommand",
        cls=NewCommand,
        brief="Enable a Command",
        description="Enables a Commmand for this Server",
        help="""This command is used to Enable any command of the Bot in the Server.
The Command should already be Disabled to Enable it Back.
Some commands like Help, Developer and Configure Commands are always Enabled.
You can also use Command Alias instead of it's Name to Enable it.""",
        usage="`enablecommand` `<command_name:str>`",
        explained_usage=["**Command Name:** Name of the Command to be Disabled."],
        permissions=["Administrator"],
        cooldown="`1`/`10 sec` - [`Guild`]",
        examples=[
            'enablecommand ping',
            'enablecommand tictactoe'
        ]
    )
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def _enablecommand(self, ctx, command_name:str):
        command = discord.utils.find(lambda cmd: cmd.name == command_name or command_name in cmd.aliases, self.client.commands)
        if not command:
            return await ctx.reply(f"{Emoji.redcross} No Such Command Found")
        elif command.name in self.non_disable_commands:
            return await ctx.reply(f"{Emoji.redcross} This command is already Enabled in this Server!")
        else:
            async with self.client.pool.acquire() as conn:
                async with conn.transaction() as trans:
                    data = await conn.fetch("SELECT * FROM guild_disabled WHERE guild_id=$1 AND command_name=$2", ctx.guild.id, command.name)
                    if not data:
                        return await ctx.reply("This command is already Enabled in this Server")
                    else:
                        await conn.execute("DELETE FROM guild_disabled WHERE guild_id=$1 AND command_name=$2;", ctx.guild.id, command.name)
                        return await ctx.reply(f"{Emoji.greentick} Successfully Enabled Command `{command.name}` for this Server")

    @_enablecommand.error
    async def _enablecommand_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, _error)
        resp = error.response()
        await ctx.reply(resp)

def setup(client):
    client.add_cog(CommandManagement(client))