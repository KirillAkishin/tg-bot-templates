import logging
logger = logging.getLogger(__name__)
import pandas as pd
from telebot.types import Message
from telebot.util import extract_arguments
from . import extra

### HANDLERS ###
class UserHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.users = db.loc.users
        self.roles = db.loc.roles
        self.groups = db.loc.groups
        
    def get_user(self, msg):
        arg = extract_arguments(msg.text)
        if arg:
            if arg.isnumeric():
                user_id = int(arg)
                if user_id not in self.users.df.index:
                    return extra.blanks['error_nouser'].format(user=user_id)
                user_dict = {j:i for i,j in zip(self.users.df.loc[user_id].to_list(), self.users.df.columns)}
                user_dict |= {'user_id': user_id}
                return user_dict
            return extra.blanks['error_request'].format(user=arg)
        user_id = msg.from_user.id
        if user_id not in self.users.df.index:
            return extra.blanks['error_nouser'].format(user=user_id)
        user_dict = {j:i for i,j in zip(self.users.df.loc[user_id].to_list(), self.users.df.columns)}
        user_dict |= {'user_id': user_id}
        return user_dict
    
    def get_role(self, msg):
        arg = extract_arguments(msg.text)
        if arg:
            if arg.isnumeric():
                user_id = int(arg)
                resp = self.get_role_uid(user_id)
                if resp:
                    return resp
                return extra.blanks['error_nouser'].format(user=user_id)
            return extra.blanks['error_request'].format(user=arg)
        user_id = msg.from_user.id
        resp = self.get_role_uid(user_id)
        if resp:
            return resp
        return extra.blanks['error_nouser'].format(user=user_id)

    def get_role_uid(self, user_id):
        if user_id not in self.users.df.index:
            return None
        role_id = int(self.users.df.loc[user_id,'role_id'])
        return self.roles.df.loc[role_id,'role_name']
    
    def get_groups(self, msg):
        arg = extract_arguments(msg.text)
        if arg:
            if arg.isnumeric():
                user_id = int(arg)
                resp = self.get_groups_uid(user_id)
                if resp:
                    return resp
                return extra.blanks['error_nouser'].format(user=user_id)
            return extra.blanks['error_request'].format(user=user_id)
        user_id = msg.from_user.id
        resp = self.get_groups_uid(user_id)
        if resp:
            return resp
        return extra.blanks['error_nouser'].format(user=user_id)
    
    def get_groups_uid(self, user_id):
        if user_id not in self.users.df.index:
            return None
        res = []
        for group_id in self.users.df.loc[user_id,'group_ids'][1:-1].split(','):
            res.append(self.groups.df.loc[int(group_id),'group_name'])
        return ','.join(res)
    
    def check_privileges(self, msg, privilege):
        user_id = int(msg.from_user.id)
        if user_id in self.users.df.index:
            role_id = self.users.df.loc[user_id,'role_id']
            return self.roles.df.loc[role_id, f'is_{privilege}']
        return False
    
    def is_dev(self, msg):
        return self.check_privileges(msg, 'dev')
    
    def is_admin(self, msg):
        return self.check_privileges(msg, 'admin')
    
    def is_auth(self, msg):
        return self.check_privileges(msg, 'auth')
    
    def is_ban(self, msg):
        return self.check_privileges(msg, 'ban')
    
    def set_role(self, user_id, role_id):
        if role_id not in self.roles.df.index:
            return False
        if user_id not in self.users.df.index:
            return False
        self.users.df.loc[user_id,'role_id'] = role_id
        self.users.write()
        logger.info(f"{user_id}'s role has been changed to '{role_id}'")
        return True
    
    def promote_to(self, msg, role_name):
        arg = extract_arguments(msg.text)
        if arg and arg.isnumeric():
            user_id = int(arg)
            if not self.check_authority(msg.from_user.id, user_id):
                return 'Error. You do not have permission to do this.'
            old_role_id = self.users.df.loc[user_id,'role_id']
            new_role_id = self.roles.df[self.roles.df['role_name']==role_name].index[0]
            if old_role_id > new_role_id:
                if self.set_role(user_id, new_role_id):
                    return None
                return f"Error. {user_id} don't exist in base."
            return f"Error. {user_id} is already a {role_name} (or higher)."
        return 'Error. Type:\n/promote2[role] [ID]'
    
    def demoted_to(self, msg, role_name):
        arg = extract_arguments(msg.text)
        if arg and arg.isnumeric():
            user_id = int(arg)
            if not self.check_authority(msg.from_user.id, user_id):
                return 'Error. You do not have permission to do this.'
            old_role_id = self.users.df.loc[user_id,'role_id']
            new_role_id = self.roles.df[self.roles.df['role_name']==role_name].index[0]
            if old_role_id < new_role_id:
                if self.set_role(user_id, new_role_id):
                    return None
                return f"Error. {user_id} don't exist in base."
            return f"Error. {user_id} is already a {role_name} (or lower)."
        return 'Error. Type:\n/demoted2[role] [ID]'
    
    def ban(self, msg):
        arg = extract_arguments(msg.text)
        if arg and arg.isnumeric():
            user_id = int(arg)
            if not self.check_authority(msg.from_user.id, user_id):
                return 'Error. You do not have permission to do this.'
            role_id = self.roles.df[self.roles.df['role_name']=='banned'].index[0]
            if self.set_role(user_id, role_id):
                return None
            return f"Error. {user_id} don't exist in base."
        return 'Error. Type:\n/ban [user_id]'
    
    def check_authority(self, subject_id, object_id):
        s_id = self.users.df.loc[subject_id,'role_id']
        o_id = self.users.df.loc[object_id,'role_id']
        if s_id < o_id:
            return True
        return False

    def _check_permission(self, is_dev,is_admin,is_moder,is_auth,is_ban, role, args):
        for m in args:
            if isinstance(m, Message):
                break
        user_id = int(m.from_user.id)
        role_id = self.users.df.loc[user_id,'role_id']
        row = self.roles.df.loc[role_id]
        return ((role == row['role_name'] if role else True) 
                and (True if is_dev is None else is_dev == row['is_dev'])
                and (True if is_admin is None else is_admin == row['is_admin'])
                and (True if is_moder is None else is_moder == row['is_moder'])
                and (True if is_auth is None else is_auth == row['is_auth'])
                and (True if is_ban is None else is_ban == row['is_ban']))
    
    def _add_user(self, user_id, role_id, group_ids='[-1]'):
        self.users.df.loc[user_id] = [role_id,group_ids]
        self.users.write()

    def identification(self, msg, new_role='guest', group_ids='[-1]'):
        user_id = int(msg.from_user.id)
        if user_id not in self.users.df.index:
            role_id = self.roles.df.reset_index().set_index('role_name').loc[new_role,'role_id']
            self.users.df.loc[user_id] = [role_id, group_ids]
            self.users.write()
            logger.info(f"{user_id} is a new user")
        logger.info(f"{user_id} has been identified")
        return user_id
    
    def authentication(self, m):
        if m.text:
            answer = m.text.lower().strip()
            if answer == 'yes':
                logger.info(f"{m.from_user.id} is authenticated")
                self.bot.send.reply(m, 'You accepted the rules.\n/help')
                self.authorization(m.from_user.id)
                return True
            if answer == '/rules':
                self.bot.send.reply(m, extra.blanks['rules'])
        self.bot.send.message(m, extra.blanks['start'])
        self.bot.register_next_step_handler(m, self.authentication)
    
    def authorization(self, user_id, new_role='user'):
        if user_id not in self.users.df.index:
            return False
        cur_role_id = int(self.users.df.loc[user_id,'role_id'])
        min_role_id = int(self.roles.df.reset_index().set_index('role_name').loc[new_role,'role_id'])
        if cur_role_id <= min_role_id:
            result = True
        else:
            result = self.set_role(user_id, min_role_id)
        if result:
            logger.info(f"{user_id} is authorizated")
        return result

    def sign_up(self, msg):
        if self.is_auth(msg):
            self.bot.send.message(msg, extra.blanks['repeated_start'])
        else:
            self.identification(msg)
            self.bot.send.reply(msg, extra.blanks['rules']) 
            self.authentication(msg)
    
