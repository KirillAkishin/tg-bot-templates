class UserManager:
    def __init__(self):
        pass
    
    def create_user(self, username, **extra_fields):
        pass
    
    def create_superuser(self, username, **extra_fields):
        pass

    
class User:
    def __init__(self, username, is_superuser=False, **extra_fields):
        self.is_superuser = is_superuser
        self.username = username
        self.first_name = None
        self.last_name = None
        self.groups = None
        self.date_joined = None
        self.last_activity = None