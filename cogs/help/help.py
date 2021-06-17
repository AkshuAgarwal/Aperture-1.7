from typing import Optional
import datetime
import asyncio

from discord import utils, Embed
from discord.ext import commands

from bot.main import NewCommand, Emoji, Paginator, reply

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")

    async def build_help(self, ctx: commands.Context):
        data = {
            "General Commands": [
                "ping", "uptime" ,"help"
            ],
            "Fun Commands": [
                "morse", "ascii"
            ],
            "Games Commands": [
                "tictactoe"
            ],
            "Currency Commands": [
                'createaccount', 'balance'
            ],
            "Admin Commands": [
                "setprefix", "enablecommand", "disablecommand", "enablechannel", "disablechannel"
            ],
            "Miscellaneous Commands": [
                'avatar'
            ],
            "Developer Commands": [
                "eval", "sql", "load", "unload", "reload"
            ],
        }
        all_commands = self.client.commands
        _embeds = []

        for key, value in data.items():
            _command_data = []
            for commands in value:
                _command = utils.find(lambda cmd: cmd.name == commands, all_commands)
                _command_data.append((_command.name, _command.brief))

            _description=f"• {ctx.prefix}"+ f"\n• {ctx.prefix}".join(f"{cmd_name} → {cmd_brief}" for (cmd_name, cmd_brief) in _command_data)
            _command_data.clear()

            embed = Embed(
                title=key,
                description=_description,
                color=0x00EEFF,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Page No. {list(data.keys()).index(key)+1}/{len(data)} • Thanks for using {ctx.guild.me.name}", icon_url=ctx.guild.me.avatar_url)
            _embeds.append(embed)
        
        pager = Paginator(
            pages=_embeds,
            timeout=150
        )
        await pager.start(ctx)


    async def get_command_help(self, ctx: commands.Context, command_name:str):
        command = utils.find(lambda cmd: cmd.name == command_name or command_name in cmd.aliases, self.client.commands)
        if command is not None:
            embed = Embed(
                title=f"Help for {command.name} Command",
                description=f"{command.description}",
                color=0x00EEFF,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Thanks for using {ctx.guild.me.name}", icon_url=ctx.guild.me.avatar_url)

            if not command.usage:
                _cmd_syntax = "None"
            else:
                _cmd_syntax = f"`{ctx.prefix}` {command.usage}"
            if not command.aliases:
                _cmd_aliases = "None"
            else:
                _cmd_aliases = ", ".join([f"`{i}`" for i in command.aliases])
            if not command.explained_usage:
                _cmd_explained_usage = "None"
            else:
                _cmd_explained_usage = "→ " + "\n→ ".join([i for i in command.explained_usage])
            if not command.permissions:
                _cmd_permissions = "None"
            else:
                _cmd_permissions = "→ " + "\n→ ".join([i for i in command.permissions])
            if not command.bot_permissions:
                _cmd_bot_permissions = "None"
            else:
                _cmd_bot_permissions = "→ " + "\n→ ".join([i for i in command.bot_permissions])
            if not command.examples:
                _cmd_examples = "None"
            else:
                _cmd_examples = f"→ {ctx.prefix}" + f"\n→ {ctx.prefix}".join([i for i in command.examples])

            embed.add_field(name=f"{Emoji.cmd_syntax} | Command Syntax",
                value=_cmd_syntax, inline=False)
            embed.add_field(name=f"{Emoji.cmd_aliases} | Aliases",
                value=_cmd_aliases, inline=False)
            embed.add_field(name=f"{Emoji.cmd_extended_help} | Extended Help",
                value=command.help if command.help is not None else "None", inline=False)
            embed.add_field(name=f"{Emoji.cmd_explained_usage} | Explained Usage",
                value=_cmd_explained_usage, inline=False)
            embed.add_field(name=f"{Emoji.cmd_permissions} | Permissions Required",
                value=_cmd_permissions, inline=False)
            embed.add_field(name=f"{Emoji.cmd_bot_permissions} | Permissions Required by Bot",
                value=_cmd_bot_permissions, inline=False)
            embed.add_field(name=f"{Emoji.cmd_cooldown} | Cooldown",
                value=command.cooldown if command.cooldown is not None else "None", inline=False)
            embed.add_field(name=f"{Emoji.cmd_examples} | Examples",
                value=_cmd_examples, inline=False)

            return await reply(self.client, ctx, f"> Tip: Use `{ctx.prefix}help --all` to get a list of all commands in your DMs!", embed=embed)
        else:
            return await reply(self.client, ctx, f"{Emoji.redcross} No Command named `{command_name}` Found!")


    @commands.command(
        name='help',
        cls= NewCommand,
        brief='Get some Help',
        description="To get Help for my Commands",
        usage="`help` `[command_name:str]` `[--all]`",
        explained_usage=[
            "**Command Name:** Name of the particular Command to get help for.",
            "**--all:** Adding `--all` after help will send you a full Command list in your DMs. Make sure you have your DMs on."
        ],
        bot_permissions=['Manage Messages'],
        cooldown='`1/5 sec` - [`User`]',
        examples=[
            'help',
            'help --all',
            'help kick',
            'help tictactoe'
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _help(self, ctx, command_name: Optional[str] = None):
        if not command_name:
            await self.build_help(ctx)
        elif command_name == '--all':
            return await reply(self.client, ctx, "Command Making is in Progress...")
        else:
            await self.get_command_help(ctx, command_name)

def setup(client):
    client.add_cog(Help(client))