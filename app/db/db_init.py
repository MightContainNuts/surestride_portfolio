import os
from sqlmodel import SQLModel, create_engine, Session, select
from app.db.models import User, Message
from datetime import datetime


class DBHandler:
    def __init__(self):
        self.engine = None
        self.session = None
        self.db_url = os.getenv("DATABASE_URL")

    def __enter__(self):
        self.create_engine()
        self.create_schema()
        self.create_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

        if self.engine:
            self.engine.dispose()
        if exc_type or exc_val or exc_tb:
            print(f"An error occurred: \n {exc_val} \n {exc_tb} \n {exc_type}")
        print("Database connection closed.")

    def create_engine(self):
        self.engine = create_engine(self.db_url, echo=True)

    def create_session(self):
        if self.engine:
            self.session = Session(self.engine)
        else:
            raise ValueError("Engine not created. Call create_engine first.")

    def create_schema(self):
        """Create the database schema (tables) if they don't exist."""
        if self.engine:
            SQLModel.metadata.create_all(self.engine)
        else:
            raise ValueError("Engine not created. Call create_engine first.")

    def get_user_by_username(self, username: str):
        """Get a user by username."""
        user = self.session.exec(select(User).where(User.username == username)).first()
        return user

    def verify_password(self, user_id:int, password: str):
        """Verify a password against the stored hashed password."""
        user = self.session.exec(select(User).where(User.user_id == user_id)).first()
        if user:
            return User.verify_password(password, user.hashed_password)
        return False

    def _add_test_user(self):
        test_user = User(
            username="test_user",
            email="<EMAIL>",
            hashed_password="hashed_password",
            created_on=datetime.now(),
        )
        self.session.add(test_user)
        self.session.commit()

if __name__ == "__main__":
    with DBHandler() as db:
        db.get_user_by_username("dean")
        db.verify_password("12345678")