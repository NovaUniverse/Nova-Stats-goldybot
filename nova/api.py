from logging import exception
import nextcord
import requests
import json

from src.goldy_utility import goldy, SimpleNamespace
from src.goldy_func import print_and_log
import src.goldy_error as goldy_error
try:
    import src.utility.msg as msg #New Goldy Bot
except ImportError:
    import utility.msg as msg #Old Goldy Bot. (I changed the folder structure in the latest goldy bot CDK.)
import settings
import config.config as config

from . import endpoints
from . import mojang
from . import msg as nova_msg

API = "https://novauniverse.net/api"
API_NAME = "Nova Universe"

VISAGE = "https://visage.surgeplay.com" #Used to render 3d png's of players.

headers = {'User-Agent': str(settings.bot_name + config.bot_version)}

async def request(web_dir, ctx=None, client=None): #Makes a request to the API. (Used as the main method to make requests to the API.)
    #Check if web server is up.
    print_and_log(None, f"Connecting to {API_NAME.upper()}...")
    try:
        response = requests.get(API + endpoints.webdirs.connection_check, headers=headers)
        data = response.json()
    except Exception as e:
        print_and_log("error", )

    try: #Except block incase the json returned is not as expected.
        if not data["success"] == True:
            if not data["success"] == False:
                if not ctx == None:
                    await goldy.log_error(ctx, client, f"{(msg.error.api).format(API_NAME)}\n API RETURNED: {data}", None)
                print_and_log("error", f"[{API_NAME.upper()} : API] Request failed.\n API RETURNED: {data}")

            return (msg.api).format(API_NAME)

    except KeyError as e:
        if not ctx == None:
            await goldy.log_error(ctx, client, f"{(msg.error.api).format(API_NAME)}\n DATA RETURNED BY API: {data}", None)
        print_and_log("error", f"[{API_NAME.upper()} : API] Request failed.\n DATA RETURNED BY API: {data}")

    #Actual request.
    print_and_log(None, f"Requesting '{web_dir}'...")
    try:
        response = requests.get(API + web_dir, headers=headers)
        data = response.json()

        #Convert json to class and return.
        data_formatted = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
        print_and_log("info_2", f"[DONE]")
        print_and_log()

        #Tries to catch an api error.
        try:
            if not ctx == None:
                if data_formatted.error == "NOT_FOUND":
                    await ctx.send(nova_msg.api.player_not_found.format(ctx.author.mention, nova_msg.emojis.nova))
                    return False

                else:
                    await ctx.send(nova_msg.api.error.format(ctx.author.mention, data_formatted.message))
                    await error.report(data_formatted)
                    return False

        except AttributeError as e:
            pass

        return data_formatted

    except Exception as e:
        if not ctx == None:
            await goldy.log_error(ctx, client, f"{(msg.error.api).format(API_NAME)} >>> {e}\n DATA RETURNED BY API: {data}", None)
        print_and_log("error", f"[{API_NAME.upper()} : API] Request failed. >>> {e}\n DATA RETURNED BY API: {data}")


class error():
    @staticmethod
    async def report(data_formatted): #Reports api error to console.
        try:
            print_and_log("warn", f"[{API_NAME.upper()} : API] Api Error. >>> {data_formatted.message}\n DATA RETURNED BY API:\n {data_formatted}")
        except AttributeError as e:
            await goldy_error.log(error=e)

class players():
    @staticmethod
    async def get(ctx=None, client=None): #Returns dictinary of all online players.
        data = await request(endpoints.webdirs.players_online, ctx, client)
        return data

class player():
    class _3d_model(): #Class that contains all methods to do with rendering 3d player skins. Example: https://visage.surgeplay.com/full/512/3442be0542114a15a10c4bdb2b6060fa
        @staticmethod
        async def render(uuid:str): #Renders a full 3d model of the player using visage.
            return VISAGE + endpoints.visage_webdirs.full.format(uuid)

    @staticmethod
    async def get(ctx, client, player_ign:str): #Returns basic infomation about the player.
        uuid = await mojang.player.uuid.convert.full_uuid(await mojang.player.uuid.find(player_ign)) #Gets uuid of player from mojang and converts it to a full uuid.
        data = await request(endpoints.webdirs.player_stats.format(uuid), ctx, client)
        if data == False:
            return False
        return data.data

class servers():
    class status(): #Returns status of servers.

        @staticmethod
        async def get(ctx=None, client=None):
            data = await request(endpoints.webdirs.extended_network_stats, ctx, client)
            return data.servers