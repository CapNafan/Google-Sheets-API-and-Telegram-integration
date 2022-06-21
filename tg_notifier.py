import requests
try:
    from tg_config import TGBOT_TOKEN, CHAT_ID
except (ModuleNotFoundError, NameError):
    print('TGBOT_TOKEN and CHAT_ID are not defined. Perhaps you did not create tg_config file')


def send_message(text):
    try:
        url_request = "https://api.telegram.org/bot" + \
                      TGBOT_TOKEN + "/sendMessage" + "?chat_id=" +\
                      CHAT_ID + "&text=" + text

        requests.get(url_request)
    except NameError:
        pass
