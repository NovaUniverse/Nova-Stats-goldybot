import nextcord
from nextcord.ext import commands
import asyncio

from goldy_func import *
from goldy_utility import *
import config.msg as msg

#Change 'your_cog' to the name you wish to call your cog. ('your_cog' is just a placeholder.)
cog_name = "nova_stats"

class nova_stats(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command() #Just an example command showing the important layout of commands in goldy bot and demoing a bit of the servers.get() function.
    async def example_command(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True: #Every command on goldy bot must have this if statement. Remember to place the command code inside the if statement.
            server_info = servers.get(ctx.guild.id) #<<< If you need to ask the server for it's configuration by any change here is the code.
            #and then you can grab what server info from the json like this below.

            server_info.roles.bot_admin #<<< gives you the id for the bot_admin role from the server this command is being ran by.
            await ctx.send("This is the bot admin role id >>> " + server_info.roles.bot_admin)

    @commands.command()
    async def starter_command(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

def setup(client):
    client.add_cog(nova_stats(client))

#Need Help? Check out this: {youtube playlist}