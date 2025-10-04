from .dao import Feature_dao, User_dao, Vote_dao, singleton
from .model import Feature, User, Vote


@singleton
class Model_dao_service:
    _user_dao: User_dao
    _feature_dao: Feature_dao
    _vote_dao: Vote_dao

    _next_ids: dict[str, int]

    _USER_IDS_KEY = "user_ids"
    _FEATURE_IDS_KEY = "feature_ids"
    _VOTE_IDS_KEY = "vote_ids"

    def __init__(self):
        self._user_dao = User_dao()
        self._feature_dao = Feature_dao()
        self._vote_dao = Vote_dao()

        self._next_ids = {}

        self._next_ids[self._USER_IDS_KEY] = 1
        self._next_ids[self._FEATURE_IDS_KEY] = 1
        self._next_ids[self._VOTE_IDS_KEY] = 1

    def add_user(self, user_name: str):
        new_User = User(self._next_ids[self._USER_IDS_KEY], user_name)
        self._user_dao.put(new_User)
        self._next_ids[self._USER_IDS_KEY] += 1

    def add_feature(self, title: str, desc: str):
        new_Feature = Feature(self._next_ids[self._FEATURE_IDS_KEY], title, desc)
        self._feature_dao.put(new_Feature)
        self._next_ids[self._FEATURE_IDS_KEY] += 1

    # TODO: проверить, что такие user_id и feature_id есть
    def add_vote(self, feature_id: int, user_id: int):
        if user_id not in self._user_dao:
            raise ApiError("there's no user with such id")
        if feture_id not in self._feature_dao:
            raise ApiError("there's no feature with such id")
        new_Vote = Vote(self._next_ids[self._VOTE_IDS_KEY], feature_id, user_id)
        self._vote_dao.put(new_Vote)
        self._next_ids[self._VOTE_IDS_KEY] += 1

    def get_all_users(self):
        return self._user_dao.get_objects()

    def get_all_features(self):
        return self._feature_dao.get_objects()

    def get_all_votes(self):
        return self._vote_dao.get_objects()
