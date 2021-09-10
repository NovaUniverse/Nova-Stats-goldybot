from os import name
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
                if option.lower() in ["status", "servers"]: #Send a overview of the Nova Universe server status.
                    async with ctx.typing(): #Types when waiting for API.
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
                servers_context = "\n"

                for server in servers_data:
                    if server.available == True:
                        availablity_icon = "💡"
                    if server.available == False:
                        availablity_icon = "❌"

                    #WORK IN PROGRESS! WHERE I LEFT OFF(09/09/2021)

                    servers_context += f"• **{availablity_icon} {server.display_name}:   🕹️``{server.player_count}``**\n"
                
                #Move odd number lines to left and even to right.
                servers_context_left = ""
                servers_context_right = ""
                max_lines = len(servers_context.splitlines())
                for num in range(0, max_lines):
                    if (num % 2) == 0: #Check if even or odd.
                        servers_context_right += (servers_context.splitlines())[num] + "\n"
                    else:
                        servers_context_left += (servers_context.splitlines())[num] + "\n"

                embed = await nova_stats.embed.create(ctx)
                embed.set_image(url="https://media.discordapp.net/attachments/876976105335177286/885874813137207338/Minecraft_2021-04-03_00_33_58.png")
                embed.add_field(name="**__🌐Server Status__:**", value=servers_context_left, inline=True)
                embed.add_field(name="**__🌐Server Status__:**", value=servers_context_right, inline=True)

                await ctx.send(embed=embed)
                
            @staticmethod
            async def overview(ctx, player_name):
                return True

def setup(client):
    client.add_cog(nova_stats(client))

#Need Help? Check out this: {youtube playlist}