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
        cooldown="`1/10 sec` - [`Guild`]",
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
            resp = f"{Emoji.redcross} No Such Command Found!"
        elif command.name in self.non_disable_commands:
            resp = f"{Emoji.redcross} This command cannot be Disabled!"
        else:
            async with self.client.pool.acquire() as conn:
                async with conn.transaction() as trans:
                    data = await conn.fetch("SELECT * FROM guild_disabled WHERE guild_id=$1;", ctx.guild.id)
                    if not data:
                        await conn.execute("INSERT INTO guild_disabled (guild_id, command_name) VALUES ($1, array[$2]);", ctx.guild.id, command.name)
                        resp = f"{Emoji.greentick} Successfully Disabled Command `{command.name}` for this Server"
                    else:
                        if data[0]['command_name'] is None:
                            await conn.execute("UPDATE guild_disabled SET command_name=array[$1] WHERE guild_id=$2;", command.name, ctx.guild.id)
                            resp = f"{Emoji.greentick} Successfully Disabled Command `{command.name}` for this Server"
                        elif command.name not in data[0]['command_name']:
                            await conn.execute("UPDATE guild_disabled SET command_name=array_append(command_name, $1) WHERE guild_id=$2;", command_name, ctx.guild.id)
                            resp = f"{Emoji.greentick} Successfully Disabled Command `{command.name}` for this Server"
                        elif command.name in data[0]['command_name']:
                            resp = f"{Emoji.redcross} This command is Already Disabled in this Server"
                        else:
                            resp = f"{Emoji.redcross} Oops! Some Error Occured..."

                    data = await conn.fetch("SELECT * FROM guild_disabled;")
                    for row in data:
                        self.client.disabled_data[row['guild_id']] = {
                            'command_name': row['command_name'],
                            'channel_id': row['channel_id']
                        }

        try:
            response = self.client.old_responses[ctx.message.id]
            return await response.edit(content=resp, embed=None, file=None, files=None, delete_after=None, allowed_mentions=None)
        except KeyError:
            response = await ctx.reply(resp)
            self.client.old_responses[ctx.message.id] = response
            return

    @_disablecommand.error
    async def _disablecommand_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, _error)
        await error.response()

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
        cooldown="`1/10 sec` - [`Guild`]",
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
            resp = f"{Emoji.redcross} No Such Command Found"
        elif command.name in self.non_disable_commands:
            resp = f"{Emoji.redcross} This command is already Enabled in this Server!"
        else:
            async with self.client.pool.acquire() as conn:
                async with conn.transaction() as trans:
                    data = await conn.fetch("SELECT * FROM guild_disabled WHERE guild_id=$1;", ctx.guild.id)
                    if not data:
                        resp = "This command is already Enabled in this Server"
                    elif command.name not in data[0]['command_name']:
                        resp = "This command is already Enabled in this Server"
                    elif command.name in data[0]['command_name']:
                        await conn.execute("UPDATE guild_disabled SET command_name=array_remove(command_name, $1) WHERE guild_id=$2;", command.name, ctx.guild.id)
                        resp = f"{Emoji.greentick} Successfully Enabled Command `{command.name}` for this Server"
                    else:
                        resp = f"{Emoji.redcross} Oops! Some Error Occured..."

                    data = await conn.fetch("SELECT * FROM guild_disabled;")
                    for row in data:
                        self.client.disabled_data[row['guild_id']] = {
                            'command_name': row['command_name'],
                            'channel_id': row['channel_id']
                        }

        try:
            response = self.client.old_responses[ctx.message.id]
            return await response.edit(content=resp, embed=None, file=None, files=None, delete_after=None, allowed_mentions=None)
        except KeyError:
            response = await ctx.reply(resp)
            self.client.old_responses[ctx.message.id] = response
            return

    @_enablecommand.error
    async def _enablecommand_error(self, ctx, error):
        _error = getattr(error, 'original', error)
        error = Errors(ctx, _error)
        await error.response()

def setup(client):
    client.add_cog(CommandManagement(client))