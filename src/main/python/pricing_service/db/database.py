from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the base class for the ORM model
ModelBase = declarative_base()


class Conn:
    """
    Encapsulates the database connection details.
    """
    def __init__(self, dbname='postgres', user='postgres', password='postgres', host="localhost", port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_db_url(self):
        """
        Returns the database connection URL.
        """
        db_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        print(f"db_url: {db_url}")
        return db_url


class PostgresDB:
    def __init__(self, conn: Conn):
        """
        Initialize the database connection and ORM session using Conn class.
        """
        self.engine = create_engine(conn.get_db_url())
        self.Session = sessionmaker(bind=self.engine)

        # Create tables if they don't exist
        ModelBase.metadata.create_all(self.engine)


class BaseDao:
    """
    Generic Data Access Object (DAO) class for fetching all records from a table.
    """
    def __init__(self, engine, model):
        self.engine = engine
        self.SessionMaker = sessionmaker(bind=self.engine)
        self.model = model

    def as_dict(self, x):
        return {c.name: getattr(x, c.name) for c in x.__table__.columns}

    def fetch_all(self):
        """
        Fetch all rows from the specified table.
        """
        session = self.SessionMaker()
        try:
            return session.query(self.model).all()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            session.close()

    def insert(self, instance):
        """
        Fetch all rows from the specified table.
        """
        self.insert_many([instance])

    def insert_many(self, instances: list):
        """
        Fetch all rows from the specified table.
        """
        session = self.SessionMaker()
        print("inserting many rows")
        try:
            session.add_all(instances)
            session.commit()
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            session.close()