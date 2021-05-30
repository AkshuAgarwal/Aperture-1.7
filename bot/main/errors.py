import discord
from discord.ext import commands
from . import Emoji as e

class Errors:
    def __init__(self, ctx, error):
        self.ctx = ctx
        self.error = error

    def response(self):
        error = self.error
        if isinstance(error, commands.MissingRequiredArgument):
            return f" {e.redcross} **Missing Required Argument(s)!**\n> Missing Parameters: `{error.param}`\n> Usage: {self.ctx.command.usage}"
        if isinstance(error, commands.TooManyArguments):
            return f"{e.redcross} **Too Many Argument(s)!**\n> Usage: {self.ctx.command.usage}"
        if isinstance(error, commands.MessageNotFound):
            return f"{e.redcross} **Message not Found!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.MemberNotFound):
            return f"{e.redcross} **Member not Found!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.GuildNotFound):
            return f"{e.redcross} **Guild not Found!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.UserNotFound):
            return f"{e.redcross} **User not Found!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.ChannelNotFound):
            return f"{e.redcross} **Message not Found!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.ChannelNotReadable):
            return f"{e.redcross} **I am Missing Permissions to read the Messages in the Channel!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.BadColourArgument):
            return f"{e.redcross} **Bad Color Argument!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.RoleNotFound):
            return f"{e.redcross} **Role not Found!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.BadInviteArgument):
            return f"{e.redcross} **Invite passed is Invallid or Expired!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.EmojiNotFound):
            return f"{e.redcross} **Emoji not Found!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.PartialEmojiConversionFailure):
            return f"{e.redcross} **Emoji passed does not match the correct Format!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.BadBoolArgument):
            return f"{e.redcross} **Invaild Boolean Argument!**\n> Argument Passed: `{error.argument}`"
        if isinstance(error, commands.BadUnionArgument):
            return f"{e.redcross} **Invalid Arguments Passed!**\n> Invaild Arguments: `{error.param}`\n> Usage: {self.ctx.command.usage}"
        if isinstance(error, commands.UnexpectedQuoteError):
            return f"{e.redcross} **Unexpected Quote Found!**\n> Unexpected Quote: `{error.quote}`"
        if isinstance(error, commands.InvalidEndOfQuotedStringError):
            return f"{e.redcross} **String Quoting Error!**\n> Invalid Characters Found: `{error.char}`"
        if isinstance(error, commands.ExpectedClosingQuoteError):
            return f"{e.redcross} **Closing Quote Expected!**\n> Quote Expected: `{error.close_quote}`"
        if isinstance(error, commands.CheckAnyFailure):
            raise error
        if isinstance(error, commands.PrivateMessageOnly):
            return f"{e.redcross} **An Operation in this command only works in Private Messages (DMs)**"
        if isinstance(error, commands.NoPrivateMessage):
            return f"{e.redcross} **An Operation in this command don't work in Private Messages (DMs)**"
        if isinstance(error, commands.NotOwner):
            return f"{e.redcross} **This is a Developer-Only Command!**"
        if isinstance(error, commands.MissingPermissions):
            missing_perms = ", ".join(f"`{i}`" for i in self.ctx.command.permissions)
            return f"**{e.redcross} You are missing Permissions to use this Command!**\n> Missing Permission(s): `{error.missing_perms}`\n> Required Permission(s): {missing_perms}"
        if isinstance(error, commands.BotMissingPermissions):
            bot_missing_perms = ", ".join(f"`{i}`" for i in self.ctx.command.bot_permissions)
            return f"**{e.redcross} I am missing some Permissions to use this Command!**\n> Missing Permission(s): `{error.missing_perms}`\n> Required Permission(s): {bot_missing_perms}"
        if isinstance(error, commands.MissingRole):
            return f"**{e.redcross} You are Missing Role to use this Command!**\n> Missing Role: `{error.missing_role}`"
        if isinstance(error, commands.BotMissingRole):
            return f"**{e.redcross} I am Missing Role to use this Command!**\n> Missing Role: `{error.missing_role}`"
        if isinstance(error, commands.MissingAnyRole):
            missing_roles = ', '.join(f"`{i}`" for i in error.missing_roles)
            return f"**{e.redcross} You are Missing some Roles to use this Command!**\n> Missing Role(s): {missing_roles}"
        if isinstance(error, commands.BotMissingAnyRole):
            bot_missing_roles = ', '.join(f"`{i}`" for i in error.missing_roles)
            return f"**{e.redcross} I am Missing some Roles to use this Command!**\n> Missing Role(s): {bot_missing_roles}"
        if isinstance(error, commands.NSFWChannelRequired):
            return f"**{e.redcross} This command is restricted to NSFW Channels only!**"
        if isinstance(error, commands.DisabledCommand):
            return f"**{e.redcross} The Command is Disabled!**"
        if isinstance(error, commands.CommandInvokeError):
            return f"**{e.redcross} Some Error occured while Invoking the Command!**\n> Error: `{error.original}`"
        if isinstance(error, commands.CommandOnCooldown):
            return f"**{e.redcross} The Command is currently on `{str(error.cooldown.type)[11:]}` Cooldown!**\n> Retry After: `{error.retry_after:,.0f} seconds`"
        if isinstance(error, commands.MaxConcurrencyReached):
            return f"**{e.redcross} The Command has reached it's Max Concurrency of `{error.number}` per `{error.per}`! Please try again after some time...**"
        if isinstance(error, commands.ExtensionAlreadyLoaded):
            return f"**{e.redcross} The Extension `{error.name}` is Already Loaded!**"
        if isinstance(error, commands.ExtensionNotLoaded):
            return f"**{e.redcross} The Extension `{error.name}` is not Loaded!**"
        if isinstance(error, commands.ExtensionFailed):
            return f"**{e.redcross} Failed to Load the Extension `{error.name}`!**\n> Error: `{error.original}`"
        if isinstance(error, commands.ExtensionNotFound):
            return f"**{e.redcross} Extension `{error.name}` not Found!**"
        if isinstance(error, (discord.Forbidden, discord.NotFound, discord.DiscordServerError)):
            raise error