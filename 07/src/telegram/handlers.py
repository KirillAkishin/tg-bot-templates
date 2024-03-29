import pandas as pd
import logging
logger = logging.getLogger(__name__)
from . import blanks

### GLOBE ###
users = pd.read_csv('./data/users/users.csv', index_col='user_id')
roles = pd.read_csv('./data/users/roles.csv', index_col='role_id')

### HANDLERS ###
class Handler:
    def __init__(self, bot, db=None):
        self.users = UserHandler(bot)
        self.sessions = SessionHandler(bot)
        self.db = db
        self.mu = None
        
class UserHandler:
    def __init__(self, bot, users=users, roles=roles):
        self.bot = bot
        self.users = users
        self.roles = roles
        
    def get_role(self, user_id):
        if user_id not in self.users.index:
            return None
        role_id = self.users.loc[user_id,'role_id']
        return self.roles.loc[role_id,'role_name']
    
    def set_role(self, user_id, role_id):
        if role_id not in self.roles.index:
            return False
        if user_id not in self.users.index:
            return False
        self.users.loc[user_id,'role_id'] = role_id
        return True
    
    def promote_to(self, msg, role_name):
        user_id = int(msg.chat.id)
        old_role_id = self.users.loc[user_id,'role_id']
        new_role_id = self.roles[self.roles['role_name']==role_name].index[0]
        if old_role_id > new_role_id:
            return self.set_role(user_id, new_role_id)
        else:
            False
    
    def identification(self, msg, new_user='guest', group_ids='[-1]'):
        user_id = int(msg.chat.id)
        if user_id not in self.users.index:
            role_id = self.roles.reset_index().set_index('role_name').loc[new_user,'role_id']
            self.users.loc[user_id] = [role_id, group_ids]
        return user_id
    
    def authorize(self, msg):
        user_id = int(msg.chat.id)
        ok = self.promote_to(user_id, 'user')
        return ok
    
    def ban(self, msg):
        user_id = int(msg.chat.id)
        role_id = self.roles[self.roles['role_name']=='banned'].index[0]
        self.users.loc[int(user_id)]['role_id'] = role_id
        return True

    
    def check_role(self, user_id, role):
        if self.users.loc[int(user_id)]['role'] == role:
            return True
        return False
    
    def is_admin(self, msg):
        if self.users.loc[int(msg.chat.id)]['is_admin']:
            return True
        return False
    
    def is_authorized(self, msg):
        if self.users.loc[int(msg.chat.id)]['is_authorized']:
            return True
        return False
        
    def set_role(self, user_id, role):
        pass
#         self.users
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
