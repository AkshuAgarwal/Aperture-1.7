from discord.ext import commands, ipc

class IPCRoutes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @ipc.server.route()
    async def get_guilds(self, data):
        return self.client.guilds

def setup(client):
    client.add_cog(IPCRoutes(client))