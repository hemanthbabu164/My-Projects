import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import Product

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_product(db_session):
    """Create a sample product for testing"""
    product = Product(
        name="Test Brake Pads",
        description="Test brake pads for testing",
        manufacturer="Test Brand",
        part_number="TEST-001",
        price=50.0,
        category="Brakes",
        stock_quantity=10
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product
