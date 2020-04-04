import json
import passlib.hash
import secrets
import time


class LoginManager:
    def __init__(self, password_file):
        self.user_list = json.load(password_file)
        self.logged_in_users = {}

    def verify(self, user, password):
        try:
            return passlib.hash.sha512_crypt.verify(password, self.user_list[user]['password'])
        except Exception:
            return False

    def is_logged_in(self, token):
        if token in self.logged_in_users.keys():
            return True
        else:
            return False

    def login(self, user, token):
        self.logged_in_users[token] = {
            'user': user,
            'access-level': self.user_list[user]["access-level"],
            'time': time.time()
        }

    @staticmethod
    def make_token():
        return secrets.token_urlsafe(128)
