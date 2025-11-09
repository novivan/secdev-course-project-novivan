from passlib.context import CryptContext
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        "username", String(50), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        "hashed_password", String(100), nullable=False
    )

    # relationship
    votes: Mapped[list["Vote"]] = relationship(
        "Vote", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, username: str, hashed_password: str):
        self.name = username
        self.hashed_password = hashed_password

    def get_id(self) -> int:
        return self.id

    def get_name(self):
        return self.name

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)


class Feature(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    title: Mapped[str] = mapped_column("title", String(100))
    desc: Mapped[str] = mapped_column("description", String(500))

    # relationship
    votes: Mapped[list["Vote"]] = relationship(
        "Vote", back_populates="feature", cascade="all, delete-orphan"
    )

    def get_id(self) -> int:
        return self.id

    def get_title(self) -> str:
        return self.title

    def get_description(self) -> str:
        return self.desc


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    feature_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("features.id", ondelete="CASCADE")
    )  # it is "value" in task description
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="votes")
    feature: Mapped["Feature"] = relationship("Feature", back_populates="votes")

    def get_id(self) -> int:
        return self.id

    def get_feature_id(self) -> int:
        return self.feature_id

    def get_user_id(self) -> int:
        return self.user_id
