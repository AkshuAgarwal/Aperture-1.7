import os
import sys
import json
import asyncio
import aiohttp
import traceback
import itertools
from datetime import datetime
from typing import Optional
from pytz import utc
from contextlib import suppress
from dotenv import load_dotenv

import asyncpg
import discord
from discord import Intents
from discord.ext import commands, tasks
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .main import is_disabled, error_handler

if sys.version_info[0] == 3 and sys.version_info[1] >= 7 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv('./.env')

with open("./data/botdata.json", "r", encoding="utf-8") as f:
    botdata = json.load(f)

async def create_pool(client, loop) -> None:
    client.pool = await asyncpg.create_pool(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
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

class Bot(BotBase):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=Intents.all(),
            strip_after_prefix=True,
            case_insensitive=True
        )

        self.ready:bool = False
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        self.old_responses:dict = {}
        self.prefixes:dict = {}
        self.disabled_data:dict = {}
        self.time_limit:int = 120
        self.launch_time = datetime.utcnow()
        self.aiohttp_session: Optional[aiohttp.ClientSession] = None

        self.COGS = list()
        for folders in os.scandir("./cogs"):
            for files in os.listdir(f"./cogs/{folders.name}"):
                if files.endswith(".py"):
                    self.COGS.append((folders.name, files))

        self.loop.create_task(self.startup())


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
                print('Database Setup Done!')

    async def cache_db(self):
        async with self.pool.acquire() as conn:
            raw_data = await conn.fetch("SELECT * FROM guild_data;")
            for row in raw_data:
                self.prefixes[row['guild_id']] = [row['prefix'], row['prefix_case_insensitive']]
            print("Cached Guild Prefixes!")
            raw_data_2 = await conn.fetch("SELECT * FROM guild_disabled;")
            for row in raw_data_2:
                self.disabled_data[row['guild_id']] = {
                    'command_name': row['command_name'],
                    'channel_id': row['channel_id']
                }
            print("Cached Guild Disabled Data!")

    @tasks.loop(seconds=540)
    async def update_presence(self):
        x = 0
        for guild in self.guilds:
            x += len(guild.members)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ap!help"))
        await asyncio.sleep(180)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{x} Members in {len(self.guilds)} Servers!"))
        await asyncio.sleep(180)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Dashboard Coming Soon..."))
        await asyncio.sleep(180)

    async def startup(self):
        await self.wait_until_ready()
        self.aiohttp_session = aiohttp.ClientSession()
        await self.setup_db()
        await self.cache_db()
        self.update_presence.start()


    def run(self, version) -> None:
        self.version = version

        print('Setting up...')
        self.setup()

        TOKEN = os.getenv('TOKEN')
        print('Running the Client...')
        super().run(TOKEN, reconnect=True)

    async def close(self) -> None:
        print("Shutting Down...")
        self.scheduler.shutdown()
        await self.aiohttp_session.close()
        await super().close()

    async def on_connect(self) -> None:
        print(f"Connected to Client. Latency: {self.latency * 1000:,.0f} ms")

    async def on_disconnect(self) -> None:
        print("Client Disconnected.")

    async def on_command_error(self, ctx, exc) -> None:
        await error_handler(ctx, exc)

    async def on_ready(self) -> None:
        if self.ready:
            return

        self.scheduler.start()
        print(f"Scheduler Started [{len(self.scheduler.get_jobs()):,} job(s) Scheduled]")

        self.ready = True
        print("Client Ready!")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        if before.content == after.content:
            return
        time_diff = after.edited_at - before.created_at
        if time_diff.seconds > self.time_limit:
            return
        await self.process_commands(after)

    async def on_message_delete(self, message) -> None:
        if message.author.bot:
            pass
        try:
            bot_response = self.old_responses[message.id]
            await bot_response.delete()
        except KeyError:
            pass

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=commands.Context)
        if ctx.command is None:
            return
        check = await is_disabled(self, ctx)
        if check is False:
            return
        await self.invoke(ctx)

    async def on_command_completion(self, ctx):
        with suppress(Exception):
            await asyncio.sleep(client.time_limit)
            client.old_responses.pop(ctx.message.id)

client = Bot()

loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool(client, loop))

# Add currencyinfo command
# Method to Add users to currency table
# Complete and check ttt with coins
# setup currency system
# Fix Avatar Command: user:Union.....
# Fix error console logging