import nextcord
from nextcord.ext import commands
import asyncio
import requests

from goldy_func import *
from goldy_utility import *
import config.msg as goldy_msg
import settings

#Importing nova_stats utilites.
from .nova import api, msg

cog_name = "nova_stats"

class nova_stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nova(self, ctx, option=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if not option == None:
                if option.lower() == "status": #Send a overview of the Nova Universe server status.
                    servers_data = await api.servers.status.get(ctx, self.client)
                    await nova_stats.pages.server_overview(ctx, servers_data)

                    return True
            
            await ctx.send((goldy_msg.help.command_usage).format(ctx.author.mention, "!nova {option}")) #Sends help.

    @commands.command(aliases=['player'])
    async def stats(self, ctx, option=None):
        if await can_the_command_run(ctx, cog_name) == True:
            #WORK IN PROGRESS
            async with ctx.typing():
                pass

    class embed():
        @staticmethod
        async def create(ctx):
            embed=nextcord.Embed(title="**__🐉Nova Stats (BETA)__**", description="Welcome to Nova Stats!", color=settings.AKI_PINK)
            return embed

    class pages():
            @staticmethod
            async def server_overview(ctx, servers_data):
                servers_context = ""

                for server in servers_data:

                    if server.available == True:
                        availablity_icon = "💡"
                    if server.available == False:
                        availablity_icon = "❌"

                        pass #WORK IN PROGRESS! WHERE I LEFT OFF(09/09/2021)

                    servers_context += f"**{availablity_icon} {server.display_name}: 🕹️``{server.player_count}`` **\n"
                    
                print(servers_context) #Remove after testing.
                
            @staticmethod
            async def overview(ctx, player_name):
                return True

def setup(client):
    client.add_cog(nova_stats(client))

#Need Help? Check out this: {youtube playlist}