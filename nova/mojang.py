import requests
import json

from src.goldy_utility import goldy, SimpleNamespace
from src.goldy_func import print_and_log
try:
    import src.utility.msg as msg #New Goldy Bot
except ImportError:
    import utility.msg as msg #Old Goldy Bot. (I changed the folder structure in the latest goldy bot CDK.)
import settings
import config.config as config

from . import endpoints

API = "https://api.mojang.com"
API_NAME = "Mojang"

headers = {'User-Agent': str(settings.bot_name + config.bot_version)}

async def request(web_dir, ctx=None, client=None): #Makes a request to the API. (Used as the main method to make requests to the API.)
    #Actual request.
    print_and_log(None, f"Requesting '{web_dir}'...")
    try:
        response = requests.get(API + web_dir, headers=headers)
        data = response.json()

        #Convert json to class and return.
        data_formatted = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
        print_and_log("info_2", f"[DONE]")
        print_and_log()
        print(data_formatted)
        return data_formatted

    except Exception as e:
        if not ctx == None:
            await goldy.log_error(ctx, client, f"{(msg.error.api).format(API_NAME)} >>> {e}\n DATA RETURNED BY API: {data}", None)
        print_and_log("error", f"[{API_NAME.upper()} : API] Request failed. >>> {e}\n DATA RETURNED BY API: {data}")

        return False

class player():
    class uuid():
        @staticmethod
        async def find(ign:str): #Get's player's uuid from ign.
            data = await request(endpoints.mojang_webdirs.player_profile.format(ign))
            return data.id

        class convert():
            @staticmethod
            async def full_uuid(short_uuid):
                return short_uuid[:8] + "-" + short_uuid[8:12] +  "-" + short_uuid[12:16] +  "-" + short_uuid[16:20] +  "-" + short_uuid[20:]

    class ign():
        @staticmethod
        async def find(uuid:str): #Get's player's ign from uuid.
            data = await request(endpoints.mojang_webdirs.player_profile.format(uuid))
            return data.name