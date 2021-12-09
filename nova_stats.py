import datetime
from os import name
import nextcord
from nextcord import colour
from nextcord.ext import commands
import asyncio
import requests

from src.goldy_func import *
from src.goldy_utility import *
try:
    import src.utility.msg as goldy_msg #New Goldy Bot
except ImportError:
    import utility.msg as goldy_msg #Old Goldy Bot. (I changed the folder structure in the latest goldy bot CDK.)
import settings

#Importing nova_stats utilites.
import importlib
from .nova import api, msg, config

cog_name = "nova_stats"
version = 1.10

class nova_stats(commands.Cog, name="🐉Nova Stats"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.version = version
        self.help_command_index = 6

        importlib.reload(api)
        importlib.reload(msg)
        importlib.reload(config)

    @commands.command(description="Allows you to check status of Nova Universe servers and who's currently online.", usage="!nova {option: status, players}")
    async def nova(self, ctx, option=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if not option == None:
                if option.lower() in ["status", "servers"]: #Send a overview of the Nova Universe server status.
                    async with ctx.typing(): #Types when waiting for API.
                        #Find server status data.
                        servers_data = await api.servers.status.get(ctx, self.client)
                    
                    #Send page.
                    await nova_stats.pages.server_overview(ctx, self.client, servers_data)
                    return True

                if option.lower() in ["players"]:
                    async with ctx.typing():
                        players_online = await api.players.get(ctx, self.client)

                    await nova_stats.pages.players_online(ctx, self.client, players_online)
                    return True
            
            await ctx.send((goldy_msg.help.command_usage).format(ctx.author.mention, "!nova {option: status, players}")) #Sends help.

    @nova.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.nova")

    @commands.command(aliases=['stats'], description="Allows you to check your and your friend's gamemode stats.", hidden=True)
    async def player(self, ctx, player:str=None, option=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if not player == None:
                if option == None: #Send player overview page.
                    async with ctx.typing():
                        #Get player's data.
                        data = await api.player.get(ctx, self.client, player)
                        if data == False: #Stops command if api fails to find data.
                            return False

                        player_render = await api.player._3d_model.render(uuid=data.uuid)
                        
                    #Send embed.
                    await nova_stats.pages.stats.player_overview(ctx, self.client, data, player_render)

                    #Send page.
                    #await ctx.send(goldy_msg.error.not_available_yet)
                    return True

                else: #Send apropiate page for option.
                    if option.lower() == "skywars": 
                        return True

            await ctx.send((goldy_msg.help.command_usage).format(ctx.author.mention, "!player {ign}")) #Sends help.

    @player.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.stats")


    class embed():
        @staticmethod
        async def create(ctx=None, title=f"**__Nova Stats (BETA)__**", description="Welcome to Nova Stats!", colour=settings.AKI_PINK):
            embed=nextcord.Embed(title=title, description=description, color=colour)
            return embed

    class pages():
        @staticmethod
        async def server_overview(ctx, client, servers_data):
            servers_context = ""

            for server in servers_data:
                if server.available == True:
                    availablity_icon = msg.emojis.status.on
                if server.available == False:
                    availablity_icon = msg.emojis.status.off

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

            server_icon = await guild_func.server_icon.get(ctx, client)

            embed = await nova_stats.embed.create(ctx)
            embed.set_author(name="Nova Universe • Status", url="https://novauniverse.net/status/", icon_url=server_icon)
            embed.set_image(url="https://media.discordapp.net/attachments/876976105335177286/885874813137207338/Minecraft_2021-04-03_00_33_58.png")
            if not servers_context_left == "":
                embed.add_field(name="**__🌐Server Status__:**", value=servers_context_left, inline=True)
            if not servers_context_right == "":
                embed.add_field(name="**__🌐Server Status__:**", value=servers_context_right, inline=True)

            await ctx.send(embed=embed)
            
        @staticmethod
        async def players_online(ctx, client, players_online):
            online_players_context = ""

            for player in players_online.players:
                print(f"{player.username}")

                online_players_context += f"• **🟢``{player.username}`` in 🌐``{player.server_type_display_name}``**\n"

            #Move odd number lines to left and even to right.
            online_players_context_left = ""
            online_players_context_right = ""
            max_lines = len(online_players_context.splitlines())
            actual_amount_of_players = max_lines
            if max_lines > config.nova.players.max_display:
                max_lines = 6
                
            for num in range(0, max_lines):
                if (num % 2) == 0: #Check if even or odd.
                    online_players_context_right += (online_players_context.splitlines())[num] + "\n" #Odd
                else: 
                    online_players_context_left += (online_players_context.splitlines())[num] + "\n" #Even

            server_icon = await guild_func.server_icon.get(ctx, client)

            embed = await nova_stats.embed.create(ctx)
            embed.set_author(name="Nova Universe • Players", url="https://novauniverse.net/status/", icon_url=server_icon)
            embed.set_image(url="https://media.discordapp.net/attachments/876976105335177286/885943940384161802/hAdWXaU_d_1.png")
            '''
            if not online_players_context_left == "":
                embed.add_field(name="**__🕹️Online Players__:**", value=online_players_context_left, inline=True)
            else:
                embed.add_field(name="**__🕹️Online Players__:**", value="***Totally a tone of players online ;)***", inline=True)
            if not online_players_context_right == "":
                embed.add_field(name="**__🕹️Online Players__:**", value=online_players_context_right, inline=True)
            '''

            if not online_players_context_right == "":
                online_players_context_combined = online_players_context_left + online_players_context_right
                if actual_amount_of_players > config.nova.players.max_display:
                    amount_of_more_players = actual_amount_of_players - config.nova.players.max_display
                    online_players_context_combined += f"\n***__and {amount_of_more_players} player(s) more...__***"
                embed.add_field(name="**__🕹️Online Players__:**", value=online_players_context_combined, inline=False)
            else:
                embed.add_field(name="**__🕹️Online Players__:**", value="***Totally a ton of players online ;)***", inline=False)

            await ctx.send(embed=embed)

        class stats:
            @staticmethod
            async def player_overview(ctx, client, data, player_render:str): #Display overall player stats.
                server_icon = await guild_func.server_icon.get(ctx, client)

                #Embed
                embed = await nova_stats.embed.create(colour=settings.GREEN)
                embed.set_author(name=f"Nova Universe • Player Stats", url="https://novauniverse.net", icon_url=server_icon)
                embed.set_image(url=player_render)
                embed.set_thumbnail(url=msg.images.nova_logo)

                if data.is_online == 1: status = f"🟢 ``Online``"
                else: status = f"🔴 ``Offline``"
                embed.add_field(name="**🎮 STATUS:**", value=status, inline=True)
                embed.add_field(name="**😊 IGN:**", value=f"``{data.username}``", inline=True)
                embed.add_field(name="**💼 FIRST JOIN:**", value=f"``{data.first_join_timestamp.date[:10]}``", inline=False)
                
                embed.set_footer(text=msg.footer.type_1.format(version))
                await ctx.send(embed=embed)

                return True

            class games:
                @staticmethod
                async def skywars(ctx, data): #Display all skywars stats.
                    pass

def setup(client):
    client.add_cog(nova_stats(client))

#Need Help? Check out this: {youtube playlist}