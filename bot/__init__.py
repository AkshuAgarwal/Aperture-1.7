import os
import json
import traceback
import asyncio
import itertools

import asyncpg
import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pytz import utc

with open("./data/credentials.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)

with open("./data/botdata.json", "r", encoding="utf-8") as f:
    botdata = json.load(f)

async def create_pool(client, loop) -> None:
    client.pool = await asyncpg.create_pool(
        host=credentials["database"]["host"],
        port=credentials["database"]["port"],
        user=credentials["database"]["user"],
        password=credentials["database"]["pswd"],
        database=credentials["database"]["db"],
        loop=loop,
        min_size=1,
        max_size=100
    )
    return client.pool

async def get_prefix(client, message):
    default_prefix = botdata["prefix"]
    if isinstance(message.channel, discord.DMChannel):
        return list(map(''.join, itertools.product(*zip(str(default_prefix).upper(), str(default_prefix).lower()))))
    else:
        async with client.pool.acquire() as conn:
            data = await conn.fetchrow("SELECT prefix, prefix_case_insensitive FROM guild_data WHERE guild_id = $1", message.guild.id)
            prefix = data["prefix"]
            case_insensitive = data["prefix_case_insensitive"]
            if case_insensitive is True:
                return list(map(''.join, itertools.product(*zip(str(prefix).upper(), str(prefix).lower()))))
            else:
                return prefix

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
        self.loop = None

        self.COGS = list()
        for folders in os.scandir("./cogs"):
            for files in os.listdir(f"./cogs/{folders.name}"):
                if files.endswith(".py"):
                    self.COGS.append((folders.name, files))

        super().__init__(
            command_prefix=get_prefix,
            intents=Intents.all(),
            strip_after_prefix=True,
            case_insensitive=True
        )

    def setup(self) -> None:
        for (folder_name, file_name) in self.COGS:
            self.load_extension(f"cogs.{folder_name}.{file_name[:-3]}")
            print(f"+[COG] --> {folder_name}/{file_name}")
        
        print(f"Loaded Cogs Successfully! Total Cogs: {len(self.COGS)}")

    async def setup_db(self):
        async with self.pool.acquire() as conn:
            async with conn.transaction() as trans:
                await conn.execute(open('./bot/main.sql').read())

    def run(self, version) -> None:
        self.version = version

        print('Setting up...')
        self.setup()

        TOKEN = credentials['token']
        print('Running the Client...')
        super().run(TOKEN, reconnect=True)
    
    async def close(self) -> None:
        print("Shutting Down...")
        self.scheduler.shutdown()
        await super().close()

    async def on_connect(self) -> None:
        print(f"Connected to Client. Latency: {self.latency * 1000:,.0f} ms")

    async def on_disconnect(self) -> None:
        print("Client Disconnected.")

    async def on_error(self, err: str, *args, **kwargs):
        if err == "on_command_error":
            await args[0].reply("Oops! Something went Wrong...")

        traceback.print_exc()

    async def on_ready(self) -> None:
        if self.ready:
            return
            
        print('Setting up Database...')
        await self.setup_db()
        print('Database Setup Done!')

        self.scheduler.start()
        print(f"Scheduler Started [{len(self.scheduler.get_jobs()):,} job(s) Scheduled]")
        
        self.ready = True
        print("Client Ready!")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        await self.process_commands(message)


    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is None:
            return

        await self.invoke(ctx)

client = Bot()

loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool(client, loop))