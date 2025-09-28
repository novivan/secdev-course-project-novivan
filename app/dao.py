from .model import Feature, Model_entity, User, Vote


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


#   TODO: connect dao to real database
class Dao:
    _objects: dict[int, Model_entity]

    def __init__(self):
        self._objects = {}

    def put(self, object: Model_entity):
        self._objects[object.get_id()] = object

    def get_objects(self):
        return self._objects


@singleton
class User_dao(Dao):
    def put(self, object: User):  # type: ignore
        self._objects[object.get_id()] = object


@singleton
class Feature_dao(Dao):
    def put(self, object: Feature):  # type: ignore
        self._objects[object.get_id()] = object


@singleton
class Vote_dao(Dao):
    _votes_by_user_id: dict[int, Model_entity]

    def __init__(self):
        self._objects = {}
        self._votes_by_user_id = {}

    # тут put другой, потому что мы считаем что люди голосуют только за одну фичу
    def put(self, object: Vote):  # type: ignore
        if object.get_user_id() in self._votes_by_user_id:
            object._id = self._votes_by_user_id[object.get_user_id()].get_id()
            self._objects[object.get_id()] = object
        else:
            self._objects[object.get_id()] = object
        self._votes_by_user_id[object.get_user_id()] = object
