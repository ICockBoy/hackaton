from bot.database.json_database import JSONDATABASE
from bot.subjects.user import User


class UsersManager:
    def __init__(self, db: JSONDATABASE):
        self.__db = db

    def get_all_users(self) -> dict:
        users = self.__db.get_field("users")
        if users is None:
            users = {}
            self.__db.save_field("users", users)
        return users

    def save_all_users(self, users: dict):
        self.__db.save_field("users", users)

    def get_user(self, user_id) -> User | None:
        users = self.get_all_users()
        if str(user_id) in users:
            return User(users[str(user_id)])
        else:
            return None

    def save_user(self, user_id, user: User):
        users = self.get_all_users()
        users[str(user_id)] = user.dump()
        self.save_all_users(users)

    def remove_user(self, user_id):
        users = self.get_all_users()
        if str(user_id) in users:
            users.pop(str(user_id))
        self.save_all_users(users)

    def user_in_database(self, user_id) -> bool:
        users = self.get_all_users()
        if str(user_id) in users:
            return True
        else:
            return False

    def user_in_register(self, user_id) -> bool:
        user = self.get_user(user_id)
        if user is None:
            return False
        if user.in_register:
            return True
        else:
            return False

