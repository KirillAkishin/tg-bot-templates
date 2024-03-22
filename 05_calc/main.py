import os
import pandas as pd
import utils
logger = utils.get_logger(__name__)
import yaml
with open("config.yml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token = cfg["telegram"]['token']  

### GLOBE ###
tg = utils.Telegram(token)
keyboard = utils.widgets.calculater
value = ""
old_value = ""

### HANDLERS ###
@tg.message_handler(commands = ["start", "calc"] )
def getmessage(message):
    global value
    if value == "":
        tg.send_message(message, "0", reply_markup=keyboard)
    else:
        tg.send_message(message, value, reply_markup=keyboard)
    
@tg.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == "no" :
        pass
    elif data == "C" :
        value = ""
    elif data == "=" :
        try:
            value = str(eval(value))
        except:
            value = "Ошибка!"
    else:
        value += data

    if value != old_value:
        if value == "":
            tg.edit_message_text(
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                text="0",
                reply_markup=keyboard)
        else:
            tg.edit_message_text(
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                text=value,
                reply_markup=keyboard)
    old_value = value
    if value == "Ошибка!": value = ""
        
@tg.message_handler(commands=["help"])
def help_processing(message):
    logger.warning('/help')
    tg.send_message(message, response_text='Помощь.')

### MAIN ###            
if __name__ == '__main__':
    tg.infinity_polling()