import os
from sqlmodel import SQLModel, create_engine, Session, select, inspect
from app.db.models import User, RAGDoc
from datetime import datetime
from dotenv import load_dotenv



class DBHandler:
    def __init__(self):
        load_dotenv()
        self.engine = None
        self.session = None
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable is not set.")

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

    def add_test_user(self):
        """add a test user to the database."""
        test_user = User(
            username="test_user",
            email="<EMAIL>",
            hashed_password="hashed_password",
            created_on=datetime.now(),
        )
        self.session.add(test_user)
        self.session.commit()
        print("Test user added to the database.")

    def add_user(self, username:str, email:str, hashed_password:str):
        """add a user to the database."""
        hashed_password = User.hash_password(hashed_password)
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            created_on=datetime.now(),
        )
        self.session.add(new_user)
        self.session.commit()
        print("User added to the database.")

    def delete_user(self, user_id:int):
        """remove the test user from the database."""
        user = self.session.exec(select(User).where(User.user_id == user_id)).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            print("Test user deleted from the database.")
        else:
            print("Test user not found in the database.")

    def add_doc_to_RAG_table(self, structured_data,embeddings):
        """Add a document to the RAG table."""
        try:
            # Ensure structured_data is not None and has all the required fields
            if not structured_data:
                print("structured_data is None or invalid")
                return None

            title = structured_data.title
            content = structured_data.content
            category = structured_data.category
            size = structured_data.size

            print(f"Saving structured data to database: {title}")
            print(f"Title: {title}")
            print(f"Category: {category}")
            print(f"Size: {size}")
            print(f"Content: {content[:20]}")

            # Ensure all required fields are non-empty
            if not all([title, content, category, size]) and len(embeddings) > 0:
                print("One or more required fields are missing in structured_data")
                return None

            new_doc = RAGDoc(
                title=title,
                content=content,
                category=category,
                size=size,
                embeddings=embeddings,
            )

            print(f"Created RAGDoc instance: {new_doc}")

            if not new_doc:
                print("Failed to create RAGDoc object.")
                return None

            self.session.add(new_doc)
            self.session.commit()

            print("Document saved successfully.")

        except Exception as e:
            print(f"Error occurred: {e}")
            self.session.rollback()

    def inspect_columns(self, table_name:str)->list:
        """
        Inspect the columns of the table.
        """
        inspector = inspect(self.engine)
        with DBHandler() as db:
            columns = [column['name'] for column in inspector.get_columns(table_name)]
        return columns

    def recreate_schema(self):
        """
        Recreate the database schema.
        """
        if self.engine:
            SQLModel.metadata.drop_all(self.engine)
            SQLModel.metadata.create_all(self.engine)
            print("Database schema recreated.")
        else:
            raise ValueError("Engine not created. Call create_engine first.")

    def fix_embeddings_column(self):
        """Add the embeddings column to the ragdoc table if it doesn't exist"""
        try:
            with self.engine.connect() as conn:
                from sqlalchemy import text

                # Check if the column exists
                result = conn.execute(text("PRAGMA table_info(ragdoc)"))
                columns = [col[1] for col in result.fetchall()]
                print(f"Current columns in ragdoc table: {columns}")

                if "embeddings" not in columns:
                    print("Adding embeddings column to ragdoc table...")
                    conn.execute(text("ALTER TABLE ragdoc ADD COLUMN embeddings BLOB"))
                    conn.commit()
                    print("Column added successfully")
                else:
                    print("Embeddings column already exists")

                # Verify
                result = conn.execute(text("PRAGMA table_info(ragdoc)"))
                updated_columns = [col[1] for col in result.fetchall()]
                print(f"Updated columns in ragdoc table: {updated_columns}")

                return "embeddings" in updated_columns
        except Exception as e:
            print(f"Error fixing schema: {e}")
            return False


if __name__ == "__main__":
    with DBHandler() as db:
        db.recreate_schema()