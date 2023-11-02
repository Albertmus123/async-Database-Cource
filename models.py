from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Note title : {self.title} >"

class User(Base):
    __tablename__="users"
    id:Mapped[str]=mapped_column(primary_key=True,nullable=False)
    username:Mapped[str]=mapped_column(nullable=False,unique=True)
    email:Mapped[str]=mapped_column(nullable=False)
    password:Mapped[str]=mapped_column(nullable=False)


    def __repr__(self) -> str:
        return f"<User username: {self.username} >"