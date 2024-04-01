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
        if m.photo and event=='RECEIVED from':
            text = m.photo[-1].file_id
        if m.video and event=='RECEIVED from':
            text = m.video.file_id
        if m.sticker and event=='RECEIVED from':
            text = m.sticker.file_id
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
    def message(self, message, text, parse_mode=None):
        return self.bot.send_message(message.chat.id, text, parse_mode=parse_mode)
    
    @timeout_decorator()
    @logger_decorator(item='markdown')
    def markdown(self, message, md_text):
        return self.bot.send_message(message.chat.id, md_text, parse_mode='Markdown')
    
    @timeout_decorator()
    @logger_decorator(item='gif')
    def animation(self, message, gif_name=None):
        if gif_name in extra.gif_ids['common']:
            gif_id = extra.gif_ids[gif_name]
        else:
            gif_name, gif_id = random.choice(list(extra.gif_ids['reply'].items()))
        return self.bot.send_animation(message.chat.id, gif_id)
    
    @timeout_decorator()
    @logger_decorator(item='sticker')
    def sticker(self, message, sticker_name=None):
        if sticker_name in extra.sticker_ids['common']:
            sticker_id = extra.sticker_ids[sticker_name]
        else:
            sticker_name, sticker_id = random.choice(list(extra.sticker_ids['reply'].items()))
        return self.bot.send_sticker(message.chat.id, sticker_id)

    @timeout_decorator()
    @logger_decorator(item='pic')
    def photo(self, message, pic_name=None, caption=None):
        if pic_name in extra.pic_ids['common']:
            pic_id = extra.pic_ids[pic_name]
        else:
            pic_name, pic_id = random.choice(list(extra.pic_ids['reply'].items()))
        return self.bot.send_photo(message.chat.id, pic_id)
    
    @timeout_decorator()
    @logger_decorator(item='video')
    def video(self, message, video_name=None):
        if video_name in extra.video_ids['common']:
            video_id = extra.video_ids[video_name]
        else:
            video_name, video_id = random.choice(list(extra.video_ids['reply'].items()))
        return self.bot.send_video(message.chat.id, video_id)
    
    @timeout_decorator()
    @logger_decorator(item='doc')
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
    def __init__(self, token, db, debug_id=None):
        super().__init__(token)
        self.send = Sender(self)
        self.user_handler = UserHandler(self, db)
        self.debug_id = debug_id
        logger.debug('bot initiated')        
        
    def infinity_polling(self, *args, **kwargs):
        logger.critical('bot restarted')
        if self.debug_id:
            self.send_message(self.debug_id, 'bot restarted')
        return super().infinity_polling(*args, **kwargs)
    
    def check_permission(self, is_dev=None, is_admin=None, is_moder=None, 
                         is_auth=True, is_ban=False, role=None):
        def decorator(func): 
            def inner(*args, **kwargs):
                if self.user_handler._check_permission(is_dev,is_admin,is_moder,
                                                       is_auth,is_ban, role, args):
                    return func(*args, **kwargs)
                else:
                    return self.send.reject(*args, **kwargs)
            return inner 
        return decorator
    
    @classmethod 
    def logger_decorator(cls, event='receive', item=None, level='warning'):
        return logger_decorator(event, item=item, level=level)
