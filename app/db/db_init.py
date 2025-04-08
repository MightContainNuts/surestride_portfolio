import os
from sqlmodel import SQLModel, create_engine, Session, select, inspect
from app.db.models import User, Documents
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os
import json



class DBHandler:
    def __init__(self):
        load_dotenv()
        self.engine = None
        self.session = None
        self.db_url = self.get_db_url()

        # Resolve the path using pathlib


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

    def get_db_url(self):
        """Get the database URL."""
        db_url = "sqlite:///db.sqlite"
        # if db_url and db_url.startswith("sqlite:///"):
        #     base_path = Path(__file__)
        #     db_path =  base_path / "app" / "db" / "db.sqlite"
        #     self.db_url = f"sqlite:///{db_path}"
        #     print(f"Resolved Database URL: {self.db_url}")
        # else:
        #     raise ValueError("DATABASE_URL environment variable is not set or invalid.")
        print(f"Database URL: {db_url}")
        return db_url

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

    def add_new_document(self, structured_data):
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
            if not all([title, content, category, size]):
                print("One or more required fields are missing in structured_data")
                return None

            new_doc = Documents(
                title=title,
                content=content,
                category=category,
                size=size,
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


    def retrieve_all_documents_from_db(self):
        """Retrieve all documents from the ragdoc table."""
        if self.engine:
            all_docs = self.session.exec(select(Documents.title,
                                                Documents.content,
                                                Documents.category)).all()
            print(f"Documents retrieved from the database. number of documents: {len(all_docs)}")

            all_docs_dict = [
                {"title": doc[0], "content": doc[1], "category": doc[2]} for doc in all_docs
            ]
            print(f"Documents retrieved from the database. number of documents: {len(all_docs)}")
            print(all_docs_dict)
            return all_docs_dict


    def store_documents_in_file(self, documents:list[dict[str:str]])->None:
        """Store documents in a file."""
        base_path =  Path(__file__).resolve().parent.parent.parent
        db_path = base_path / "app" / "static" / "files" / "documents.json"

        with open(db_path, "w", encoding='utf-8') as json_file:
            json.dump(documents, json_file, ensure_ascii=False,indent = 4)
        print("Documents stored in documents.json. number of documents: ", len(documents))

if __name__ == "__main__":
    with DBHandler() as db:
        docs = db.retrieve_all_documents_from_db()
        db.store_documents_in_file(docs)