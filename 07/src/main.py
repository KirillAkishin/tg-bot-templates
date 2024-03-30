import logging
import logging.config
logging.config.fileConfig('logging.conf')
import os
import pandas as pd
import utils
import telegram as tg
from telebot import types
from database import DataBase
import yaml
with open("config.yaml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    data_dir = cfg['path']['cache']
    db_params = cfg['database']
    token_file = cfg["telegram"]['token_file']

### GLOBE ###
logger = logging.getLogger(__name__)
db = DataBase(db_params)
with open(token_file) as token:
    bot = tg.Bot(token.read())

### FUNCTIONS ###
def job(message):
    import time
    time.sleep(1.5)
    return None

### HANDLERS ###
@bot.message_handler(commands=['test'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_developer=True)
def cmd_test(msg):
    bot.send.message(msg, 'ok')

@bot.message_handler(commands=['start'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_authorized=None)
def cmd_start(msg):
    bot.user_handler.identification(msg)
    resp = bot.send.reply(msg, tg.extra.blanks['start'])
    bot.register_next_step_handler(resp, bot.user_handler.registration)

@bot.message_handler(commands=['rules'])
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_rules(msg):
    bot.send.message(msg, tg.extra.blanks['rules'])

@bot.message_handler(commands=["help"])
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_help(msg):
    bot.send.message(msg, 'Помощь.')

@bot.message_handler(commands=["settings"])
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_help(msg):
    bot.send.widget_keyboard(msg, 'Choose your settings', [['A','B'],[1,2,3],['/help']])

@bot.message_handler(commands=['my_role'])
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_my_role(msg):
    resp = bot.user_handler.get_role(msg.chat.id)
    bot.send.message(msg, resp)

@bot.message_handler(commands=["my_groups"])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_my_groups(msg):
    resp = bot.user_handler.get_groups(msg.chat.id)
    bot.send.message(msg, resp)

@bot.message_handler(regexp="/.*")
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_unknown(msg):
    bot.send.message(msg, 'Такой команды нет.\n/help')

@bot.message_handler(content_types='animation')
@bot.logger_decorator(item='gif')
@bot.check_permission()
def msg_animation(msg):
    bot.send.animation(msg)

@bot.message_handler(content_types=['audio','document','photo','sticker','video','voice'])
@bot.logger_decorator(item='object')
@bot.check_permission()
def msg_unknown(msg):
    bot.send.message(msg, 'Формат сообщения не поддерживается.\n/help')

@bot.message_handler(content_types=["text"])
@bot.logger_decorator(item='message')
@bot.check_permission()
def msg_text(msg):
    bot.send.message(msg, 'Обработка запроса.')
    result = job(msg)
    if result:
        bot.send.document(msg, result)
    else:
        bot.send.message(msg, f'Ошибка.\n/help\n/start')

### MAIN ###
if __name__ == '__main__':
    bot.infinity_polling()
