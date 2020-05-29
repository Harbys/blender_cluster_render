import json
import passlib.hash
import secrets
import time


# servers login manager used to authenticate users on dashboard
class LoginManager:
    # expects a json file with users and their password hash
    def __init__(self, password_file):
        self.user_list = json.load(password_file)
        self.logged_in_users = {}

    # verifies user by username and password
    def verify(self, user, password):
        try:
            return passlib.hash.sha512_crypt.verify(password, self.user_list[user]['password'])
        except Exception:
            return False

    # verifies user by token
    def is_logged_in(self, token):
        if token in self.logged_in_users.keys():
            return True
        else:
            return False

    # logs in a user by connecting together token to username, their privilege level and login time
    def login(self, user, token):
        self.logged_in_users[token] = {
            'user': user,
            'access-level': self.user_list[user]["access-level"],
            'time': time.time()
        }

    # returns a 128 char long token
    @staticmethod
    def make_token():
        return secrets.token_urlsafe(128)
