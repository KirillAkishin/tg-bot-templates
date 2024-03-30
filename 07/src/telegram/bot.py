import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import time
import random
import numpy as np
from .handlers import UserHandler
from . import extra
import logging
logger = logging.getLogger(__name__)  
        
### UTILITY ###
# def error_handler():

def logger_decorator(event='send', item=None, level='info'):
    def decorator(func): 
        def inner(*args, **kwargs): 
            logger_record(args, event=event, item=item, level=level)
            return func(*args, **kwargs)
        return inner 
    return decorator

def logger_record(args, event, item=None, level='info'):
    def trim_text(text):
        return f"'{' '.join(text.replace('\n',' ').replace('\t',' ')[:50].split())}'" 
    for m in args:
        if isinstance(m, Message):
            break
    user = f'{m.from_user.id}:{m.from_user.username[:15].strip()}'
    if event == 'send':
        event = 'sent to'
        item = 'a ' + (item if item else 'message') + '.'
        text = ''
        for t in args:
            if isinstance(t, str):
                text = trim_text(t)
                item = item[:-1] + ':'
                break
    if event == 'receive':
        event = 'RECEIVED from'
        item = 'a ' + (item if item else 'message') + ':'
        text = trim_text(m.text) if m.text else ''
    if text == '':
        if m.animation and event=='RECEIVED from':
            text = m.animation.file_id
        else:
            item = item.replace(':','.')
    rec = f"bot {event:<15s} {user:<30s} {item:<15s} {text}".strip()
    return getattr(logger, level)(rec)

### CUSTOM TELEBOT ###
class Sender:
    def __init__(self, bot):
        self.bot = bot
        self._last_activity = time.time() 
        
    def timeout_decorator(timeout=0.5):
        def decorator(func): 
            def inner(self, *args, **kwargs): 
                t = (self._last_activity + timeout) - time.time()
                time.sleep(max(0,t))
                self._last_activity = time.time()
                return func(self, *args, **kwargs)
            return inner 
        return decorator

    @timeout_decorator()
    @logger_decorator()
    def message(self, message, text):
        return self.bot.send_message(message.chat.id, text)
    
    @timeout_decorator()
    @logger_decorator(item='gif')
    def animation(self, message, gif_name=None):
        if gif_name in extra.gif_ids['common']:
            gif_id = extra.gif_ids[gif_name]
        else:
            gif_name, gif_id = random.choice(list(extra.gif_ids['okay'].items()))
        return self.bot.send_animation(message.chat.id, gif_id)
    
    @timeout_decorator()
    @logger_decorator(item='document')
    def document(self, message, file):
        return self.bot.send_document(message.chat.id, file)
    
    @timeout_decorator()
    @logger_decorator(item='keyboard')
    def widget_keyboard(self, message, text, button_table):
        widget = ReplyKeyboardMarkup(resize_keyboard=True)
        for args in [tuple([KeyboardButton(str(i)) for i in row]) for row in button_table]:
            widget.row(*args)
        return self.bot.send_message(message.chat.id, text, reply_markup=widget)
    
    @timeout_decorator()
    @logger_decorator(item='reply')
    def reply(self, *args, **kwargs):
        return self.bot.reply_to(*args, **kwargs)
    
    @timeout_decorator(timeout=2)
    @logger_decorator(item='reject', level='warning')
    def reject(self, msg, text='access denied'):
        return self.bot.send_message(msg.chat.id, text)

class Bot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.send = Sender(self)
        self.user_handler = UserHandler(self)
        logger.debug('bot initiated')        
        
    def infinity_polling(self, *args, **kwargs):
        logger.critical('bot restarted')
        return super().infinity_polling(*args, **kwargs)
    
    def check_permission(self, is_developer=None, is_admin=None, is_authorized=True, is_banned=False, role=None):
        def decorator(func): 
            def inner(*args, **kwargs):
                if self.user_handler._check_permission(
                    is_developer,is_admin,is_authorized,is_banned,role, args):
                    return func(*args, **kwargs)
                else:
                    return self.send.reject(*args, **kwargs)
            return inner 
        return decorator
    
    @classmethod 
    def logger_decorator(cls, event='receive', item=None, level='warning'):
        return logger_decorator(event, item=item, level=level)
