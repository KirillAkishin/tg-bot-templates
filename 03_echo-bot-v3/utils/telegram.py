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
    
    def send_message(self, message, response_text=None):
        logger.info(response_text)
        self.bot.send_message(message.chat.id, response_text)