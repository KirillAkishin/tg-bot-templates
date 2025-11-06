import logging
import logging.config
logging.config.fileConfig('configs/logging.conf')
import os
import pandas as pd
import utils
import telegram as tg
from telebot.util import extract_arguments
from database import DataBase
import yaml
with open("configs/config.yaml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token_file = cfg["telegram"]['token_file']
    db_params = cfg['database']
    debug_id = cfg["telegram"]['debugging_chat_id']

### GLOBE ###
logger = logging.getLogger(__name__)
db = DataBase(db_params)
with open(token_file) as token:
    bot = tg.Bot(token.read(), db, debug_id)
    
### FUNCTIONS ###
def mock_job(message):
    import time
    time.sleep(1.5)
    return None

### HANDLERS ###
@bot.message_handler(commands=['start'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_auth=None)
def cmd_start(msg):
    bot.user_handler.sign_up(msg)

@bot.message_handler(commands=["help"])
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_help(msg):
    bot.send.message(msg, tg.extra.blanks['help'])
    
@bot.message_handler(commands=["settings"])
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_settings(msg):
    bot.send.widget_keyboard(msg, tg.extra.blanks['settings'], [['A','B'],[1,2,3],['/help']])
    
@bot.message_handler(commands=['rules'])
@bot.logger_decorator(item='command')
@bot.check_permission()
def cmd_rules(msg):
    bot.send.message(msg, tg.extra.blanks['rules'])
    
## DEVELOPING ##
@bot.message_handler(commands=['id'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_dev=True)
def cmd_chat(msg):
    bot.send.message(msg, str(msg.chat.id))
    
@bot.message_handler(commands=['test'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_dev=True)
def cmd_test(msg):
    bot.user_handler._add_user(777, 5)
    print(bot.user_handler.users.df)
    bot.send.message(msg, 'ok')
    
## ADMINING-roles ##
@bot.message_handler(commands=['promote2admin'])
@bot.logger_decorator(item='command')
@bot.check_permission(role='owner')
def cmd_promote2admin(msg):
    err = bot.user_handler.promote_to(msg, 'admin')
    if err is None:
        bot.send.message(msg, 'ok')
    else:
        bot.send.message(msg, err)
        
@bot.message_handler(commands=['promote2moder'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_promote2moder(msg):
    err = bot.user_handler.promote_to(msg, 'moder')
    if err is None:
        bot.send.message(msg, 'ok')
    else:
        bot.send.message(msg, err)
        
@bot.message_handler(commands=['promote2vip'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_moder=True)
def cmd_promote2vip(msg):
    err = bot.user_handler.promote_to(msg, 'vip')
    if err is None:
        bot.send.message(msg, 'ok')
    else:
        bot.send.message(msg, err)
        
@bot.message_handler(commands=['demoted2moder'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_demoted2moder(msg):
    err = bot.user_handler.demoted_to(msg, 'moder')
    if err is None:
        bot.send.message(msg, 'ok')
    else:
        bot.send.message(msg, err)
        
@bot.message_handler(commands=['demoted2user'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_moder=True)
def cmd_demoted2user(msg):
    err = bot.user_handler.demoted_to(msg, 'user')
    if err is None:
        bot.send.message(msg, 'ok')
    else:
        bot.send.message(msg, err)
        
@bot.message_handler(commands=['ban'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_moder=True)
def cmd_ban(msg):
    err = bot.user_handler.ban(msg)
    if err:
        return bot.send.message(msg, err)
    return bot.send.message(msg, 'ok')
    
## ADMINING-info ##
@bot.message_handler(commands=['admin'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_users(msg):
    bot.send.widget_keyboard(msg, 'Панель быстрого доступа для админиов.',
                             [
                                 ['/rules'],
                                 ['/help'],
                                 ['/ban','/promote2vip'],
                                 ['/demoted2user','/promote2moder'],
                                 ['/demoted2moder','/promote2admin'],
                                 ['/users','/roles','/groups'],
                                 ['/user','/role','/group'],
                             ])
    
@bot.message_handler(commands=['users'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_users(msg):
    bot.send.markdown(msg, str(bot.user_handler.users))
    
@bot.message_handler(commands=['roles'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_roles(msg):
    bot.send.markdown(msg, str(bot.user_handler.roles))
    
@bot.message_handler(commands=['groups'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_groups(msg):
    bot.send.markdown(msg, str(bot.user_handler.groups))
    
@bot.message_handler(commands=['user'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_user(msg):
    resp = bot.user_handler.get_user(msg)
    bot.send.message(msg, str(resp))
    
@bot.message_handler(commands=['role'])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_role(msg):
    resp = bot.user_handler.get_role(msg)
    bot.send.message(msg, resp)
    
@bot.message_handler(commands=["group"])
@bot.logger_decorator(item='command')
@bot.check_permission(is_admin=True)
def cmd_groups(msg):
    resp = bot.user_handler.get_groups(msg)
    bot.send.message(msg, resp)
    
## NOT-COMMANDS ##
@bot.message_handler(content_types='sticker')
@bot.logger_decorator(item='sticker')
@bot.check_permission()
def msg_sticker(msg):
    bot.send.sticker(msg)

@bot.message_handler(content_types='photo')
@bot.logger_decorator(item='pic')
@bot.check_permission()
def msg_photo(msg):
    bot.send.photo(msg)
    
@bot.message_handler(content_types='animation')
@bot.logger_decorator(item='gif')
@bot.check_permission()
def msg_animation(msg):
    bot.send.animation(msg)
    
@bot.message_handler(content_types=['video'])
@bot.logger_decorator(item='video')
@bot.check_permission()
def msg_video(msg):
    bot.send.video(msg)
    
@bot.message_handler(content_types=["text"])
@bot.logger_decorator(item='message')
@bot.check_permission()
def msg_text(msg): 
    bot.send.message(msg, tg.extra.blanks['processing'])
    result = mock_job(msg)
    if result:
        bot.send.document(msg, result)
    else:
        bot.send.message(msg, tg.extra.blanks['error_request'])
        
@bot.message_handler(content_types=['audio','document','voice'])
@bot.logger_decorator(item='object')
@bot.check_permission()
def msg_unknown(msg):
    bot.send.message(msg, tg.extra.blanks['msg_unknown'])
        
@bot.message_handler(regexp="/.*")
@bot.logger_decorator(item='bad-command')
@bot.check_permission()
def cmd_unknown(msg):
    bot.send.message(msg, tg.extra.blanks['cmd_unknown'])

### MAIN ###            
if __name__ == '__main__':
    bot.infinity_polling()