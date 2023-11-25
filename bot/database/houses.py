from bot.config import admins
from bot.database.json_database import JSONDATABASE
from bot.subjects.house import House


class HousesDatabase:
    def __init__(self, db: JSONDATABASE):
        self.__db = db

    def get_all_houses(self) -> dict:
        return self.__db.read()

    def get_house(self, house_name: str) -> House | None:
        house = self.__db.get_field(house_name)
        if house is None:
            return None
        return House(house)

    def set_house(self, house_name: str, house: House):
        self.__db.save_field(house_name, house.dump())

    def add_user(self, house_name: str, user_id):
        house = self.get_house(house_name)
        if house is None:
            return None
        if str(user_id) not in house.users:
            house.users.append(str(user_id))
            self.set_house(house_name, house)

    def remove_user(self, house_name: str, user_id):
        house = self.get_house(house_name)
        if house is None:
            return None
        if str(user_id) in house.users:
            house.users.remove(str(user_id))
            self.set_house(house_name, house)

    def find_user_house(self, user_id) -> str | None:
        houses = self.get_all_houses()
        for house_name, house_dict in houses.items():
            if str(user_id) in house_dict["users"]:
                return house_name
        else:
            return None

    def find_house_from_group_id(self, group_id: int) -> str | None:
        houses = self.get_all_houses()
        for house_name, house_dict in houses.items():
            if int(group_id) == house_dict["users_group_id"]:
                return house_name
        else:
            return None
