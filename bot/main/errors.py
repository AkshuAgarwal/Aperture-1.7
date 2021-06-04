import discord
from discord.ext import commands
from . import Emoji as e

class Errors:
    def __init__(self, ctx, error):
        self.ctx = ctx
        self.error = error

    async def response(self):
        error = self.error
        if isinstance(error, commands.MissingRequiredArgument):
            await self.ctx.reply(f" {e.redcross} **Missing Required Argument(s)!**\n> Missing Parameters: `{error.param}`\n> Usage: {self.ctx.command.usage}")
        if isinstance(error, commands.TooManyArguments):
            await self.ctx.reply(f"{e.redcross} **Too Many Argument(s)!**\n> Usage: {self.ctx.command.usage}")
        if isinstance(error, commands.MessageNotFound):
            await self.ctx.reply(f"{e.redcross} **Message not Found!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.MemberNotFound):
            await self.ctx.reply(f"{e.redcross} **Member not Found!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.GuildNotFound):
            await self.ctx.reply(f"{e.redcross} **Guild not Found!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.UserNotFound):
            await self.ctx.reply(f"{e.redcross} **User not Found!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.ChannelNotFound):
            await self.ctx.reply(f"{e.redcross} **Message not Found!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.ChannelNotReadable):
            await self.ctx.reply(f"{e.redcross} **I am Missing Permissions to read the Messages in the Channel!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.BadColourArgument):
            await self.ctx.reply(f"{e.redcross} **Bad Color Argument!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.RoleNotFound):
            await self.ctx.reply(f"{e.redcross} **Role not Found!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.BadInviteArgument):
            await self.ctx.reply(f"{e.redcross} **Invite passed is Invallid or Expired!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.EmojiNotFound):
            await self.ctx.reply(f"{e.redcross} **Emoji not Found!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.PartialEmojiConversionFailure):
            await self.ctx.reply(f"{e.redcross} **Emoji passed does not match the correct Format!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.BadBoolArgument):
            await self.ctx.reply(f"{e.redcross} **Invaild Boolean Argument!**\n> Argument Passed: `{error.argument}`")
        if isinstance(error, commands.BadUnionArgument):
            await self.ctx.reply(f"{e.redcross} **Invalid Arguments Passed!**\n> Invaild Arguments: `{error.param}`\n> Usage: {self.ctx.command.usage}")
        if isinstance(error, commands.UnexpectedQuoteError):
            await self.ctx.reply(f"{e.redcross} **Unexpected Quote Found!**\n> Unexpected Quote: `{error.quote}`")
        if isinstance(error, commands.InvalidEndOfQuotedStringError):
            await self.ctx.reply(f"{e.redcross} **String Quoting Error!**\n> Invalid Characters Found: `{error.char}`")
        if isinstance(error, commands.ExpectedClosingQuoteError):
            await self.ctx.reply(f"{e.redcross} **Closing Quote Expected!**\n> Quote Expected: `{error.close_quote}`")
        if isinstance(error, commands.CheckAnyFailure):
            raise error
        if isinstance(error, commands.PrivateMessageOnly):
            await self.ctx.reply(f"{e.redcross} **An Operation in this command only works in Private Messages (DMs)**")
        if isinstance(error, commands.NoPrivateMessage):
            await self.ctx.reply(f"{e.redcross} **An Operation in this command don't work in Private Messages (DMs)**")
        if isinstance(error, commands.NotOwner):
            await self.ctx.reply(f"{e.redcross} **This is a Developer-Only Command!**")
        if isinstance(error, commands.MissingPermissions):
            missing_perms = ", ".join(f"`{i}`" for i in error.missing_perms)
            required_perms = ", ".join(f"`{i}`" for i in self.ctx.command.permissions)
            await self.ctx.reply(f"**{e.redcross} You are missing Permissions to use this Command!**\n> Missing Permission(s): `{missing_perms}`\n> Required Permission(s): {required_perms}")
        if isinstance(error, commands.BotMissingPermissions):
            bot_missing_perms = ", ".join(f"`{i}`" for i in error.missing_perms)
            bot_required_perms = ", ".join(f"`{i}`" for i in self.ctx.command.bot_permissions)
            await self.ctx.reply(f"**{e.redcross} I am missing some Permissions to use this Command!**\n> Missing Permission(s): `{bot_missing_perms}`\n> Required Permission(s): {bot_required_perms}")
        if isinstance(error, commands.MissingRole):
            await self.ctx.reply(f"**{e.redcross} You are Missing Role to use this Command!**\n> Missing Role: `{error.missing_role}`")
        if isinstance(error, commands.BotMissingRole):
            await self.ctx.reply(f"**{e.redcross} I am Missing Role to use this Command!**\n> Missing Role: `{error.missing_role}`")
        if isinstance(error, commands.MissingAnyRole):
            missing_roles = ', '.join(f"`{i}`" for i in error.missing_roles)
            await self.ctx.reply(f"**{e.redcross} You are Missing some Roles to use this Command!**\n> Missing Role(s): {missing_roles}")
        if isinstance(error, commands.BotMissingAnyRole):
            bot_missing_roles = ', '.join(f"`{i}`" for i in error.missing_roles)
            await self.ctx.reply(f"**{e.redcross} I am Missing some Roles to use this Command!**\n> Missing Role(s): {bot_missing_roles}")
        if isinstance(error, commands.NSFWChannelRequired):
            await self.ctx.reply(f"**{e.redcross} This command is restricted to NSFW Channels only!**")
        if isinstance(error, commands.DisabledCommand):
            await self.ctx.reply(f"**{e.redcross} The Command is Disabled!**")
        if isinstance(error, commands.CommandInvokeError):
            await self.ctx.reply(f"**{e.redcross} Some Error occured while Invoking the Command!**\n> Error: `{error.original}`")
        if isinstance(error, commands.CommandOnCooldown):
            await self.ctx.reply(f"**{e.redcross} The Command is currently on `{str(error.cooldown.type)[11:]}` Cooldown!**\n> Retry After: `{error.retry_after:,.0f} seconds`")
        if isinstance(error, commands.MaxConcurrencyReached):
            await self.ctx.reply(f"**{e.redcross} The Command has reached it's Max Concurrency of `{error.number}` per `{error.per}`! Please try again after some time...**")
        if isinstance(error, commands.ExtensionAlreadyLoaded):
            await self.ctx.reply(f"**{e.redcross} The Extension `{error.name}` is Already Loaded!**")
        if isinstance(error, commands.ExtensionNotLoaded):
            await self.ctx.reply(f"**{e.redcross} The Extension `{error.name}` is not Loaded!**")
        if isinstance(error, commands.ExtensionFailed):
            await self.ctx.reply(f"**{e.redcross} Failed to Load the Extension `{error.name}`!**\n> Error: `{error.original}`")
        if isinstance(error, commands.ExtensionNotFound):
            await self.ctx.reply(f"**{e.redcross} Extension `{error.name}` not Found!**")
        if isinstance(error, (discord.Forbidden, discord.NotFound, discord.DiscordServerError)):
            raise error

        raise error