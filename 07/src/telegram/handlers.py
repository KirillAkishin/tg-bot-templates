import logging
logger = logging.getLogger(__name__)
from . import blanks

class Handler:
    def __init__(self, bot, db=None):
        self.users = UserHandler(bot)
        self.sessions = SessionHandler(bot)
        self.db = db
        self.mu = None
        
class UserHandler:
    def __init__(self, bot):
        self.bot = bot
    def set_role(self, message, role):
        pass
#         logger.info(f"{message.chat.id}'s role has been changed to '{role}'")
    def identification(self, message): 
        pass
#         logger.info(f"{message.chat.id} has been identified")
    def authentication(self, message):
        pass
#         logger.info(f"{message.chat.id} authenticates")
    def authorization(self, message):
        pass
#         logger.info(f"{message.chat.id} is authorizated")
    def registration(self, message):
        pass
#         logger.warning(message.text)
        answer = message.text.lower().strip()
        if answer == 'yes':
            self.authentication(message)
            self.authorization(message)
            return self.bot.reply_to(message, 'You accepted the rules.')
        if answer == '/rules':
            self.bot.send.message(message, blanks.rules)    
        self.bot.send.message(message, blanks.start_alt)
        self.bot.register_next_step_handler(message, self.registration)

        
class SessionHandler:
    def __init__(self, bot):
        self.bot = bot
    def check(self, message):
        ok = True
        return ok
