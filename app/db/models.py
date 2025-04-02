from sqlmodel import Field, SQLModel, create_engine, Session, Relationship
from passlib.context import CryptContext
from datetime import datetime
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_on: datetime = Field(default_factory=datetime.now)

    @staticmethod
    def hash_password(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def get_id(self):
        return str(self.user_id)

class Message(SQLModel, table=True):
    message_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    messages: str = Field(nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    user: User = Relationship(back_populates="messages")



# if __name__ == "__main__":
#     # Create the database engine
#     db_url = os.getenv("DATABASE_URL")
#     print(f"Connecting to database at {db_url}")
#     engine = create_engine(db_url, echo=True)
#     print(f"Connecting to database at {db_url}")
#
#     # Create the tables
#     SQLModel.metadata.create_all(engine)