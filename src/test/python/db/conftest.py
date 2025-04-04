import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pricing_service.db import ModelBase, PostgresDB, Conn
from pricing_service.model.db import KnownProductDao, LocalListingDao

@pytest.fixture
def test_db():
    """
    Creates an in-memory SQLite database for testing and returns a PostgresDB instance.
    """
    # Use SQLite in-memory database for testing
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)

    # Create tables in the test database
    ModelBase.metadata.create_all(engine)

    class TestDB(PostgresDB):
        """A subclass of PostgresDB that overrides the engine for testing."""
        def __init__(self):
            self.engine = engine
            self.Session = Session

    return TestDB()

@pytest.fixture
def known_products_dao(test_db):
    return KnownProductDao(test_db.engine)

@pytest.fixture
def local_listing_dao(test_db):
    return LocalListingDao(test_db.engine)
