from bot.config import admins
from bot.database.json_database import JSONDATABASE


class AdminDatabase:
    def __init__(self, db: JSONDATABASE):
        self.__db = db

    def is_admin(self, chat_id) -> bool:
        admins_json = self.__db.get_field("admins")
        if admins_json is None:
            admins_json = []
        if chat_id in admins_json or chat_id in admins:
            return True
        else:
            return False

    def add_admin(self, chat_id):
        admins_json = self.__db.get_field("admins")
        if admins_json is None:
            admins_json = []
        admins_json.append(chat_id)
        self.__db.save_field("admins", admins_json)

    def set_auth_token(self, token):
        tokens = self.__db.get_field("admin_tokens")
        if tokens is None:
            tokens = []
        tokens.append(token)
        self.__db.save_field("admin_tokens", tokens)

    def has_auth_token(self, token):
        tokens = self.__db.get_field("admin_tokens")
        if tokens is None:
            return False
        if token in tokens:
            return True
        else:
            return False

    def delete_auth_token(self, token):
        tokens = self.__db.get_field("admin_tokens")
        if tokens is not None:
            tokens.remove(token)
            self.__db.save_field("admin_tokens", tokens)
