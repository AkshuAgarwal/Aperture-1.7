from discord.ext.commands import Command

class NewCommand(Command):
    def __init__(self, func, **kwargs):
        self._examples = kwargs.get('examples', None)
        self._permissions = kwargs.get('permissions', None)
        self._bot_permissions = kwargs.get('bot_permissions', None)
        self._cooldown = kwargs.get('cooldown', None)
        self._explained_usage = kwargs.get('explained_usage', None)

        super().__init__(func=func, **kwargs)

    @property
    def examples(self):
        return self._examples

    @property
    def permissions(self):
        return self._permissions

    @property
    def bot_permissions(self):
        return self._bot_permissions

    @property
    def cooldown(self):
        return self._cooldown

    @property
    def explained_usage(self):
        return self._explained_usage