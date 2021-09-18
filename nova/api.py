import requests
import json

from goldy_utility import goldy, SimpleNamespace
from goldy_func import print_and_log
import config.msg as msg
import settings

from . import endpoints

API = "https://novauniverse.net/api"
API_NAME = "Nova Universe"

headers = {'User-Agent': str(settings.bot_name + settings.bot_version)}

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
        return data_formatted

    except Exception as e:
        if not ctx == None:
            await goldy.log_error(ctx, client, f"{(msg.error.api).format(API_NAME)} >>> {e}\n DATA RETURNED BY API: {data}", None)
        print_and_log("error", f"[{API_NAME.upper()} : API] Request failed. >>> {e}\n DATA RETURNED BY API: {data}")

    pass

class players():
    @staticmethod
    async def get(ctx=None, client=None): #Returns dictinary of all online players.
        data = await request(endpoints.webdirs.players_online, ctx, client)
        return data


class servers():
    class status(): #Returns status of servers.
        @staticmethod
        async def get(ctx=None, client=None):
            data = await request(endpoints.webdirs.extended_network_stats, ctx, client)
            return data.servers