import os
import json
import traceback
import asyncio
import itertools
from pytz import utc

import asyncpg
import discord
from discord import Intents
from discord.ext import commands, ipc
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .main import is_disabled

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
        try:
            data = client.prefixes[message.guild.id]
            prefix = data[0]
            if data[1] is True:
                return list(map(''.join, itertools.product(*zip(str(prefix).upper(), str(prefix).lower()))))
            else:
                return prefix
        except KeyError:
            async with client.pool.acquire() as conn:
                raw_data = await conn.fetch("SELECT * FROM guild_data;")
                client.prefixes.clear()
                for row in raw_data:
                    client.prefixes[row['guild_id']] = [row['prefix'], row['prefix_case_insensitive']]
                try:
                    data = client.prefixes[message.guild.id]
                    prefix = data[0]
                    if data[1] is True:
                        return list(map(''.join, itertools.product(*zip(str(prefix).upper(), str(prefix).lower()))))
                    else:
                        return prefix
                except KeyError:
                    async with conn.transaction() as trans:
                        await conn.execute("INSERT INTO guild_data (guild_id, prefix, prefix_case_insensitive) VALUES ($1, $2, true);", message.guild.id, default_prefix)
                        return list(map(''.join, itertools.product(*zip(str(default_prefix).upper(), str(default_prefix).lower()))))

# async def get_prefix(client, message):
#     default_prefix = botdata["prefix"]
#     if isinstance(message.channel, discord.DMChannel):
#         return list(map(''.join, itertools.product(*zip(str(default_prefix).upper(), str(default_prefix).lower()))))
#     else:
#         async with client.pool.acquire() as conn:
#             data = await conn.fetchrow("SELECT prefix, prefix_case_insensitive FROM guild_data WHERE guild_id = $1;", message.guild.id)
#             if not data:
#                 return default_prefix
#             else:
#                 prefix = data["prefix"]
#                 case_insensitive = data["prefix_case_insensitive"]
#                 if case_insensitive is True:
#                     return list(map(''.join, itertools.product(*zip(str(prefix).upper(), str(prefix).lower()))))
#                 else:
#                     return prefix

class _IPCBot(BotBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key=credentials["ipc_secret_key"])
        self.load_extension("cogs.dashboard.dashboard_ipc")

    async def on_ready(self):
        print("Client [IPC Class] Ready!")

    async def on_ipc_ready(self):
        print("IPC Server Ready!")

    async def on_ipc_error(self, endpoint, error):
        print(f"IPCError -- Endpoint: {endpoint} - Error: {error}")

class Bot(_IPCBot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=Intents.all(),
            strip_after_prefix=True,
            case_insensitive=True
        )

        self.ready = False
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
        # self.loop = None

        self.COGS = list()
        for folders in os.scandir("./cogs"):
            for files in os.listdir(f"./cogs/{folders.name}"):
                if files.endswith(".py") and files != "dashboard_ipc.py":
                    self.COGS.append((folders.name, files))

        self.loop.create_task(self.cache_prefix())

    def setup(self) -> None:
        for (folder_name, file_name) in self.COGS:
            self.load_extension(f"cogs.{folder_name}.{file_name[:-3]}")
            print(f"+[COG] --> {folder_name}/{file_name}")

        self.load_extension('jishaku')
        
        print(f"Loaded Cogs Successfully! Total Cogs: {len(self.COGS)}")

    async def setup_db(self):
        async with self.pool.acquire() as conn:
            async with conn.transaction() as trans:
                await conn.execute(open('./bot/main.sql').read())

    async def cache_prefix(self):
        await self.wait_until_ready()
        self.prefixes = {}
        async with self.pool.acquire() as conn:
            raw_data = await conn.fetch("SELECT * FROM guild_data;")
            for row in raw_data:
                self.prefixes[row['guild_id']] = [row['prefix'], row['prefix_case_insensitive']]
            print("Cached Guild Prefixes!")

    def run(self, version) -> None:
        self.version = version

        print('Setting up...')
        self.setup()
        self.ipc.start()

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
        else:
            check = await is_disabled(self, ctx)
            if check is False:
                return

        await self.invoke(ctx)

client = Bot()

loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool(client, loop))