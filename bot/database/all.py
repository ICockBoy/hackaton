from bot.database.admin import AdminDatabase
from bot.database.houses import HousesDatabase
from bot.database.json_database import JSONDATABASE
from bot.database.users_manager import UsersManager


class All:
    def __init__(self):
        self.__db_users_manager = JSONDATABASE("database/jsons/db_users_manager.json")
        self.users_manager = UsersManager(self.__db_users_manager)
        self.__db_admin = JSONDATABASE("database/jsons/admin.json")
        self.admin = AdminDatabase(self.__db_admin)
        self.__db_houses = JSONDATABASE("database/jsons/houses.json")
        self.houses = HousesDatabase(self.__db_houses)
