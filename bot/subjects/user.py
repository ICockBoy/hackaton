class User:
    fio: str = ""
    apartment: str = ""
    floor: str = ""
    entrance: str = ""
    in_register: bool = True
    number: str = ""

    def __init__(self, user: dict = None):
        if user is not None:
            self.fio = user["fio"]
            self.apartment = user["apartment"]
            self.floor = user["floor"]
            self.entrance = user["entrance"]
            self.in_register = user["in_register"]
            self.number = user["number"]

    def dump(self):
        return {
            "fio": self.fio,
            "apartment": self.apartment,
            "floor": self.floor,
            "entrance": self.entrance,
            "in_register": self.in_register,
            "number": self.number

        }
