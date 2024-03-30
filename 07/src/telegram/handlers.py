import pandas as pd
import logging
from telebot.types import Message
logger = logging.getLogger(__name__)
from . import extra

### GLOBE ###
users = pd.read_csv('./data/users/users.csv', index_col='user_id')
roles = pd.read_csv('./data/users/roles.csv', index_col='role_id')
groups = pd.read_csv('./data/users/groups.csv', index_col='group_id')

### HANDLERS ###
class UserHandler:
    def __init__(self, bot, users=users, roles=roles, groups=groups):
        self.bot = bot
        self.users = users
        self.roles = roles
        self.groups = groups        
        
    def get_role(self, user_id):
        if user_id not in self.users.index:
            return None
        role_id = self.users.loc[user_id,'role_id']
        return self.roles.loc[role_id,'role_name']
    
    def get_groups(self, user_id):
        if user_id not in self.users.index:
            return None
        res = []
        for group_id in self.users.loc[user_id,'group_ids'][1:-1].split(','):
            res.append(self.groups.loc[int(group_id),'group_name'])
        return ','.join(res)
    
    def is_developer(self, msg):
        user_id = int(msg.from_user.id)
        if user_id in self.users.index:
            if self.users.loc[user_id,'is_developer']:
                return True
        return False
    
    def is_admin(self, msg):
        user_id = int(msg.from_user.id)
        if user_id in self.users.index:
            if self.users.loc[user_id,'is_admin']:
                return True
        return False
    
    def is_authorized(self, msg):
        user_id = int(msg.from_user.id)
        if user_id in self.users.index:
            if self.users.loc[user_id,'is_authorized']:
                return True
        return False
    
    def is_banned(self, msg):
        user_id = int(msg.from_user.id)
        if user_id in self.users.index:
            if self.users.loc[user_id,'is_banned']:
                return True
        return False
    
    def identification(self, msg, new_user='guest', group_ids='[-1]'):
        user_id = int(msg.from_user.id)
        if user_id not in self.users.index:
            role_id = self.roles.reset_index().set_index('role_name').loc[new_user,'role_id']
            self.users.loc[user_id] = [role_id, group_ids]
        logger.info(f"{user_id} has been identified")
        return user_id
    
    def authentication(self, user_id):
        logger.info(f"{user_id} authenticates")
    
    def authorization(self, user_id):
        logger.info(f"{user_id} is authorizated")
    
    def set_role(self, user_id, role_id):
        if role_id not in self.roles.index:
            return False
        if user_id not in self.users.index:
            return False
        self.users.loc[user_id,'role_id'] = role_id
        logger.info(f"{user_id}'s role has been changed to '{role}'")
        return True
    
    def promote_to(self, msg, role_name):
        user_id = int(msg.from_user.id)
        old_role_id = self.users.loc[user_id,'role_id']
        new_role_id = self.roles[self.roles['role_name']==role_name].index[0]
        if old_role_id > new_role_id:
            return self.set_role(user_id, new_role_id)
        return False
    
    def ban(self, msg):
        user_id = int(msg.from_user.id)        
        role_id = self.roles[self.roles['role_name']=='banned'].index[0]
        return self.set_role(user_id, role_id)

    def _check_permission(self, is_developer,is_admin,is_authorized,is_banned,role, args):
        for m in args:
            if isinstance(m, Message):
                break
        user_id = int(m.from_user.id)
        role_id = self.users.loc[user_id,'role_id']
        row = self.roles.loc[role_id]
        return ((role == row['role_name'] if role else True) 
                and (True if is_developer is None else is_developer == row['is_developer'])
                and (True if is_admin is None else is_admin == row['is_admin'])
                and (True if is_authorized is None else is_authorized == row['is_authorized'])
                and (True if is_banned is None else is_banned == row['is_banned']))


    
    
    
    def registration(self, args):
        for m in args:
            if isinstance(m, Message):
                break
        logger.warning(m.text)
        answer = m.text.lower().strip()
        if answer == 'yes':
            self.authentication(m)
            self.authorization(m)
            return self.bot.send.reply(m, 'You accepted the rules.')
        if answer == '/rules':
            self.bot.send.message(m, extra.blanks['rules'])    
        self.bot.send.message(m, extra.blanks['start_alt'])
        self.bot.register_next_step_handler(m, self.registration)

        

