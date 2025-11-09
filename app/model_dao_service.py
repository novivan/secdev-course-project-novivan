import re

from .dao import Feature_dao, User_dao, Vote_dao
from .model import Feature, User, Vote


class Model_dao_service:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    user_dao: User_dao
    feature_dao: Feature_dao
    vote_dao: Vote_dao

    next_ids: dict[str, int]

    USER_IDS_KEY = "user_ids"
    FEATURE_IDS_KEY = "feature_ids"
    VOTE_IDS_KEY = "vote_ids"

    def __init__(self):
        self.user_dao = User_dao.get_instance()
        self.feature_dao = Feature_dao.get_instance()
        self.vote_dao = Vote_dao.get_instance()

        self.next_ids = {}

        self.next_ids[self.USER_IDS_KEY] = 1
        self.next_ids[self.FEATURE_IDS_KEY] = 1
        self.next_ids[self.VOTE_IDS_KEY] = 1

    def add_user(self, username: str, user_hashsed_password: str):
        if username is None:
            raise ValueError("username is required")
        uname = username.strip()
        if not re.fullmatch(r"[A-Za-z0-9_]{3,50}", uname):
            raise ValueError(
                "username must be 3-50 chars: letters, digits or underscore"
            )
        if not user_hashsed_password:
            raise ValueError("hashed password is required")

        user = User(username=uname, hashed_password=user_hashsed_password)
        self.user_dao.put(user)

    def add_feature(self, title: str, desc: str):
        new_Feature = Feature(title=title, desc=desc)
        self.feature_dao.put(new_Feature)
        self.next_ids[self.FEATURE_IDS_KEY] += 1

    # TODO: проверить, что такие user_id и feature_id есть
    def add_vote(self, feature_id: int, user_id: int):
        if user_id not in self.user_dao.get_objects():
            raise Exception("there's no user with such id")
        if feature_id not in self.feature_dao.get_objects():
            raise Exception("there's no feature with such id")
        new_Vote = Vote(feature_id=feature_id, user_id=user_id)
        self.vote_dao.put(new_Vote)
        self.next_ids[self.VOTE_IDS_KEY] += 1

    def get_all_users(self):
        return self.user_dao.get_objects()

    def get_all_features(self):
        return self.feature_dao.get_objects()

    def get_all_votes(self):
        return self.vote_dao.get_objects()

    def get_user_by_username(self, username: str) -> User | None:
        return self.user_dao.get_by_username(username)


mds = Model_dao_service()
