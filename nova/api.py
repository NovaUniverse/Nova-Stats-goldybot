import requests

from goldy_utility import *
import config.msg as msg
import settings

from . import endpoints

API = "https://novauniverse.net/api"
API_NAME = "Nova Universe"

headers = {'User-Agent': str(settings.bot_name + settings.bot_version)}

async def request(web_dir, ctx=None, client=None): #Makes a request to the API. (Used as the main method to make requests to the API.)
    #Check if web server is up.
    try:
        response = requests.get(API + endpoints.webdirs.connection_check, headers=headers)
        data = response.json()
    except Exception as e:
        print_and_log("error", )

    try: #Except block incase the json returned is not as expected.
        if not data["success"] == True:
            if not data["success"] == False:
                if not ctx == None:
                    await goldy.log_error(ctx, client, f"{(msg.api).format(API_NAME)}\n API RETURNED: {data}", None)
                print_and_log("error", f"[{API_NAME.upper()} : API] Request failed.\n API RETURNED: {data}")

            return (msg.api).format(API_NAME)

    except KeyError as e:
        if not ctx == None:
            await goldy.log_error(ctx, client, f"{(msg.api).format(API_NAME)}\n DATA RETURNED BY API: {data}", None)
        print_and_log("error", f"[{API_NAME.upper()} : API] Request failed.\n DATA RETURNED BY API: {data}")

    #Actual request.
    try:
        response = requests.get(API + web_dir, headers=headers)
        data = response.json()

        #Convert json to class and return.
        data_formatted = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
        return data_formatted

    except Exception as e:
        if not ctx == None:
            await goldy.log_error(ctx, client, f"{(msg.api).format(API_NAME)} >>> {e}\n DATA RETURNED BY API: {data}", None)
        print_and_log("error", f"[{API_NAME.upper()} : API] Request failed. >>> {e}\n DATA RETURNED BY API: {data}")


    pass