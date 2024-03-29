import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import time
import numpy as np
from .handlers import UserHandler
import logging
logger = logging.getLogger(__name__)  
        
### UTILITY ###
# def error_handler():
print(UserHandler)

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
        text = trim_text(m.text)
    rec = f"bot {event:<15s} {user:<30s} {item:<20s} {text}".strip()
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

class Bot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.send = Sender(self)
        self.user_handler = UserHandler(self)
        logger.debug('bot initiated')        
        
    def infinity_polling(self, *args, **kwargs):
        logger.critical('bot restarted')
        return super().infinity_polling(*args, **kwargs)
    
    @classmethod 
    def logger_decorator(cls, event='receive', item=None, level='warning'):
        return logger_decorator(event, item=item, level=level)
    
    @classmethod 
    def check(role):
        def decorator(func): 
            def inner(*args, **kwargs): 
                return func(*args, **kwargs)
            return inner 
        return decorator
    
