from sqlalchemy.orm import Session

from . import SessionLocal
from .model import Feature, User, Vote


class Dao:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __del__(self):
        self.db.close()


class User_dao(Dao):
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def put(self, object: User):
        if not getattr(object, "name", None):
            raise ValueError("Username cannot be None")
        try:
            self.db.add(object)
            self.db.commit()
            self.db.refresh(object)
        except Exception:
            self.db.rollback()
            raise

    def get_objects(self):
        users = self.db.query(User).all()
        return {user.id: user for user in users}

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.name == username).first()


class Feature_dao(Dao):
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def put(self, object: Feature):
        self.db.add(object)
        self.db.commit()
        self.db.refresh(object)

    def get_objects(self):
        features = self.db.query(Feature).all()
        return {feature.id: feature for feature in features}


class Vote_dao(Dao):
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def put(self, object: Vote):
        try:
            existing_vote = (
                self.db.query(Vote).filter(Vote.user_id == object.user_id).first()
            )
            if existing_vote:
                # only update feature_id for existing user's vote — do NOT touch id
                existing_vote.feature_id = object.feature_id
                self.db.commit()
                self.db.refresh(existing_vote)
                return existing_vote
            else:
                self.db.add(object)
                self.db.commit()
                self.db.refresh(object)
                return object
        except Exception:
            # ensure session usable after errors
            self.db.rollback()
            raise

    def get_objects(self):
        votes = self.db.query(Vote).all()
        return {vote.id: vote for vote in votes}
