class House:
    users = []
    users_group_id: int = None
    users_group_topics: dict = {}
    moderate_group_id: int = None
    moderate_topic_register: int = None
    moderate_topic_reports: int = None
    moderate_topic_requests: int = None

    def __init__(self, house: dict = None):
        if house is not None:
            self.users = house["users"]
            self.users_group_id = house["users_group_id"]
            self.users_group_topics = house["users_group_topics"]
            self.moderate_group_id = house["moderate_group_id"]
            self.moderate_topic_register = house["moderate_topic_register"]
            self.moderate_topic_reports = house["moderate_topic_reports"]
            self.moderate_topic_requests = house["moderate_topic_requests"]

    def dump(self) -> dict:
        return {
            "users": self.users,
            "users_group_id": self.users_group_id,
            "users_group_topics": self.users_group_topics,
            "moderate_group_id": self.moderate_group_id,
            "moderate_topic_register": self.moderate_topic_register,
            "moderate_topic_reports": self.moderate_topic_reports,
            "moderate_topic_requests": self.moderate_topic_requests,
        }
