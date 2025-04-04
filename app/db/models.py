from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
import bcrypt

class User(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_on: datetime = Field(default_factory=datetime.now)
    messages: list["Message"] = Relationship(back_populates="user")


    @staticmethod
    def hash_password(plain_password):
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


    def get_id(self):
        return str(self.user_id)

class Message(SQLModel, table=True):
    message_id: int | None = Field(default=None, primary_key=True)
    messages: str = Field(nullable=False)
    user_id: int = Field(foreign_key="user.user_id")
    user: User = Relationship(back_populates="messages")


class RAGDoc(SQLModel, table=True):
    doc_id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    size: int
    created_on: datetime = Field(default_factory=datetime.now)


