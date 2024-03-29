import logging
import logging.config
logging.config.fileConfig('logging.conf')
import os
import pandas as pd
import utils
import telegram as tg
from database import DataBase
import yaml
with open("config.yaml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token = cfg["telegram"]['token']  
    data_dir = cfg['path']['cache']
    db_params = cfg['database']

### GLOBE ###
logger = logging.getLogger(__name__)
db = DataBase(db_params)
bot = tg.Bot(token)
h = tg.Handler(bot)
# users = utils.users.UserManager(db.get('users'))
users = pd.read_csv('./data/users/users.csv', index_col='user_id')
print(users)

### FUNCTIONS ###
def job(message):
    import time
    time.sleep(1.5)
    return None

### HANDLERS ###
# @h.session.check
# @h.user.identification
@bot.message_handler(commands=['test'])
@bot.logger_decorator(item='command')
def cmd_rules(msg):
    print(msg)
#     if bot.user_handler.is_authorized(msg):
#         bot.send.widget_keyboard(msg, 'test', [['but1',2,3],[4,5,6]])
#     else:
#         print('error')

@bot.message_handler(commands=['my_role'])
@bot.logger_decorator(item='command')
def cmd_my_role(msg):
    resp = bot.user_handler.get_role(msg.chat.id)
    bot.send.message(msg, resp)
    
@bot.message_handler(commands=['rules'])
@bot.logger_decorator(item='command')
def cmd_rules(msg):
    bot.send.message(msg, tg.blanks.rules)
    
@bot.message_handler(commands=['start'])
@bot.logger_decorator(item='command')
def cmd_start(msg):
    h.users.identification(msg)
    response = bot.send.reply(msg, tg.blanks.start)
    bot.register_next_step_handler(response, h.users.registration)

@bot.message_handler(commands=["help"])
@bot.logger_decorator(item='command')
def cmd_help(msg):
    bot.send.message(msg, 'Помощь.')
    
@bot.message_handler(commands=["settings"])
@bot.logger_decorator(item='command')
def cmd_help(msg):
    bot.send.widget_keyboard(msg, 'Choose your settings', [['A','B'],[1,2,3],['/help']])
    
@bot.message_handler(commands=["role"])
@bot.logger_decorator(item='command')
def cmd_role(msg):
    if h.sessions.check(msg):
        bot.send.message(msg, 'Your role is "{}"'.format('impostor'))
    else:
        bot.send.message(msg, 'access denied')
    
@bot.message_handler(commands=["groups"])
@bot.logger_decorator(item='command')
def cmd_groups(msg):
    result = get_excel_from_file(msg)
    bot.send.document(msg, result)
    
@bot.message_handler(content_types=["text"])
@bot.logger_decorator(item='message')
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