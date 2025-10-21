from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Model_entity:
    _id: int

    def get_id(self):
        return self._id


class User(Model_entity):
    _name: str
    _hashed_password: str

    def __init__(self, identificator: int, name: str):
        self._id = identificator
        self._name = name
        self._hashed_password = ""

    def get_name(self):
        return self._name

    def verify_password(self, plain_password: str) -> bool:
        if not self._hashed_password:
            return False
        return pwd_context.verify(plain_password, self._hashed_password)


class Feature(Model_entity):
    _title: str
    _desc: str

    def __init__(self, identificator: int, feature_title: str, description: str):
        self._id = identificator
        self._title = feature_title
        self._desc = description

    def get_title(self):
        return self._title

    def get_description(self):
        return self._desc


class Vote(Model_entity):
    _feature_id: int  # it is "value" in task description
    _user_id: int

    def __init__(self, vote_id, feature_identificator, user_identificator):
        self._id = vote_id
        self._feature_id = feature_identificator
        self._user_id = user_identificator

    def get_feature_id(self):
        return self._feature_id

    def get_user_id(self):
        return self._user_id
