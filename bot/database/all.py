from bot.database.json_database import JSONDATABASE
from bot.database.users_manager import UsersManager


class All:
    def __init__(self):
        self.__db_users_manager = JSONDATABASE("database/jsons/db_users_manager.json")
        self.users_manager = UsersManager(self.__db_users_manager)
