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
keyboard = utils.widgets.calc_reply
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
    
@tg.message_handler(commands=['remove_keyboard'])
def remove_keyboard(message):
    value = ""
    old_value = ""
    tg.send_message(message, 'disable', reply_markup=utils.widgets.keyboard_rm)
    
@tg.message_handler(func=lambda message: message.text == '0')
def write_to_support(message):
    tg.bot.register_next_step_handler(message, save_username)
        
@tg.message_handler(commands=["help"])
def help_processing(message):
    logger.warning('/help')
    tg.send_message(message, response_text='Помощь.')

### MAIN ###            
if __name__ == '__main__':
    tg.infinity_polling()