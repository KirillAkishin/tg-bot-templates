import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import time
import numpy as np
import logging
logger = logging.getLogger(__name__)  
    
# 1. декоратор, который считает время выполнения программы для logging
# 2. остальное (то что более очевидно)
    
def logger_decorator(event=None, item=None, level='info'):
    def decorator(func): 
        def inner(*args, **kwargs): 
            logger_record(args, event=event, item=item, level=level)
            return func(*args, **kwargs)
        return inner 
    return decorator

def logger_record(args, event=None, item=None, level='info'):
    for m in args:
        if isinstance(m, Message):
            bot = 'bot'
            event = event if event else 'sent to'
            user = f'{m.from_user.id}:{m.from_user.username[:15].strip()}'
            item = item if item else 'a message:'
            text = f"'{' '.join(m.text.replace('\n',' ').replace('\t',' ')[:50].split())}'"
            rec = f"{bot} {event:<15s} {user:<30s} {item} {text}"
            return getattr(logger, level)(rec)
    
class Sender:
    def __init__(self, bot, timeout):
        self.bot = bot
        self.timeout = timeout
        self._last = time.time() 
        
    def timeout_decorator(func): 
        def inner(self, *args, **kwargs): 
            t = (self._last + self.timeout) - time.time()
            time.sleep(max(0,t))
            self._last = time.time()
            func(self, *args, **kwargs)
        return inner 
    
    @timeout_decorator
    @logger_decorator()
    def message(self, message, text):
        return self.bot.send_message(message.chat.id, text)
    
    @timeout_decorator
    @logger_decorator(item='document')
    def document(self, message, file):
        return self.bot.send_document(message.chat.id, file)
    
    @timeout_decorator
    @logger_decorator(item='keyboard')
    def widget_keyboard(self, message, text, button_table):
        widget = ReplyKeyboardMarkup(resize_keyboard=True)
        for args in [tuple([KeyboardButton(str(i)) for i in row]) for row in button_table]:
            widget.row(*args)
        return self.bot.send_message(message.chat.id, text, reply_markup=widget)

class Bot(telebot.TeleBot):
    def __init__(self, token, timeout=0.5):
        super().__init__(token)
        self.send = Sender(self, timeout=timeout)
        logger.debug('bot initiated')        
        
    def infinity_polling(self, *args, **kwargs):
        logger.critical('bot restarted')
        return super().infinity_polling(*args, **kwargs)
    
    def reply_to(self, *args, **kwargs):
        logger_record(args)
        return super().reply_to(*args, **kwargs)
    
    @classmethod 
    def logger_decorator(cls, event='received from', item=None, level='warning'):
        return logger_decorator(event=event, item=item, level=level)
    
