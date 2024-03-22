from . import app_logger
logger = app_logger.get_logger(__name__)
import telebot
        
class Telegram:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
    def infinity_polling(self, *args, **kwargs):
        logger.critical('restart')
        return self.bot.infinity_polling(*args, **kwargs)

    def message_handler(self, *args, **kwargs): 
        return self.bot.message_handler(*args, **kwargs)
    
    def send_message(self, message, response_text, **kwargs):
        logger.info(response_text)
        self.bot.send_message(message.chat.id, response_text, **kwargs)
        
    def edit_message_text(self, *args, **kwargs):
        return self.bot.edit_message_text(*args, **kwargs)
    
    def callback_query_handler(self, *args, **kwargs):
        return self.bot.callback_query_handler(*args, **kwargs)
        
    def send_document(self, message, file):
        self.bot.send_document(message.chat.id, file)