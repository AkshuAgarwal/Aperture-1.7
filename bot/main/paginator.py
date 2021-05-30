import asyncio
from typing import List, Union, Optional
from contextlib import suppress

import discord


class Paginator:
    """A pagination wrapper that allows to move between multiple pages by using reactions.
    Attributes
    ------------
    pages: Optional[Union[:class:`List[discord.Embed]`, :class:`discord.Embed`]]
        A list of pages you want the paginator to paginate.
        Passing a discord.Embed instance will still work as if you were
        using: await ctx.send(embed=embed).
    timeout: :class:`float`.
        The timeout to wait before stopping the paginator session.
        Defaults to ``90.0``.
    compact: :class:`bool`.
        Whether the paginator should only use three reactions:
        previous, stop and next. Defaults to ``False``.
    has_input: :class:`bool`.
        Whether the paginator should add a reaction for taking input
        numbers. Defaults to ``True``.
    """

    __slots__ = (
        "pages",
        "timeout",
        "compact",
        "has_input",
        "message",
        "ctx",
        "bot",
        "loop",
        "current",
        "previous",
        "end",
        "reactions",
        "__tasks",
        "__is_running",
    )

    def __init__(
        self,
        *,
        pages: Optional[Union[List[discord.Embed], discord.Embed]] = None,
        compact: bool = False,
        timeout: float = 90.0,
        has_input: bool = True,
    ):
        self.pages = pages
        self.compact = compact
        self.timeout = timeout
        self.has_input = has_input

        self.ctx = None
        self.bot = None
        self.loop = None
        self.message = None

        self.current = 0
        self.previous = 0
        self.end = 0
        self.reactions = {
            "⏮": 0.0,
            "◀": -1,
            "⏹️": "stop",
            "▶": +1,
            "⏭": None,
        }

        self.__tasks = []
        self.__is_running = True

        if self.has_input is True:
            self.reactions["🔢"] = "input"

        if self.pages is not None:
            if len(self.pages) == 2:
                self.compact = True

        if self.compact is True:
            keys = ("⏮", "⏭", "🔢")
            for key in keys:
                del self.reactions[key]

    def go_to_page(self, number):
        if number > int(self.end):
            page = int(self.end)
        else:
            page = number - 1
        self.current = page

    async def controller(self, react):
        if react == "stop":
            await self.stop()

        elif react == "input":
            to_delete = []
            message = await self.ctx.send("Which page do you want to jump to?")
            to_delete.append(message)

            def check(m):
                if m.author.id != self.ctx.author.id:
                    return False
                if self.ctx.channel.id != m.channel.id:
                    return False
                if not m.content.isdigit():
                    return False
                return True

            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
            except asyncio.TimeoutError:
                to_delete.append(
                    await self.ctx.send("You took too long to respond!")
                )
                await asyncio.sleep(5)
            else:
                to_delete.append(message)
                if int(message.content) < 1 or int(message.content) > len(self.pages):
                    await self.ctx.send(f"`{int(message.content)}` is not a vaild Page no.", delete_after=5)
                else:
                    self.go_to_page(int(message.content))

            with suppress(Exception):
                await self.ctx.channel.delete_messages(to_delete)

        elif isinstance(react, int):
            self.current += react
            if self.current < 0 or self.current > self.end:
                self.current -= react
        else:
            self.current = int(react)

    # https://discordpy.readthedocs.io/en/latest/api.html#discord.RawReactionActionEvent
    def check(self, payload):
        if payload.message_id != self.message.id:
            return False
        if payload.user_id != self.ctx.author.id:
            return False

        return str(payload.emoji) in self.reactions

    async def add_reactions(self):
        for reaction in self.reactions:
            with suppress(discord.Forbidden, discord.HTTPException):
                await self.message.add_reaction(reaction)

    async def paginator(self):
        with suppress(discord.HTTPException, discord.Forbidden, IndexError):
            self.message = await self.ctx.reply(embed=self.pages[0])

        if len(self.pages) > 1:
            self.__tasks.append(self.loop.create_task(self.add_reactions()))
        else:
            return

        while self.__is_running:
            with suppress(Exception):
                tasks = [
                    asyncio.ensure_future(
                        self.bot.wait_for("raw_reaction_add", check=self.check)
                    ),
                    asyncio.ensure_future(
                        self.bot.wait_for("raw_reaction_remove", check=self.check)
                    ),
                ]

                done, pending = await asyncio.wait(
                    tasks, timeout=self.timeout, return_when=asyncio.FIRST_COMPLETED
                )

                for task in pending:
                    task.cancel()

                if len(done) == 0:
                    # Clear reactions once the timeout has elapsed
                    return await self.stop(timed_out=True)

                payload = done.pop().result()
                reaction = self.reactions.get(str(payload.emoji))

                with suppress(Exception):
                    await self.message.remove_reaction(str(payload.emoji), payload.member)

                self.previous = self.current
                await self.controller(reaction)

                if self.previous == self.current:
                    continue

                with suppress(Exception):
                    await self.message.edit(embed=self.pages[self.current])

    async def stop(self, *, timed_out=False):
        with suppress(discord.HTTPException, discord.Forbidden):
            await self.message.clear_reactions()

        with suppress(Exception):
            self.__is_running = False
            for task in self.__tasks:
                task.cancel()
            self.__tasks.clear()

    async def start(self, ctx):
        """Start paginator session.
        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context to use.
        """
        self.ctx = ctx
        self.bot = ctx.bot
        self.loop = ctx.bot.loop

        if isinstance(self.pages, discord.Embed):
            return await self.ctx.reply(embed=self.pages)

        if not isinstance(self.pages, (list, discord.Embed)):
            raise TypeError(
                "Can't paginate an instance of <class '%s'>."
                % self.pages.__class__.__name__
            )

        if len(self.pages) == 0:
            raise RuntimeError("Can't paginate an empty list.")

        self.end = float(len(self.pages) - 1)
        if self.compact is False:
            self.reactions["⏭"] = self.end
        self.__tasks.append(self.loop.create_task(self.paginator()))