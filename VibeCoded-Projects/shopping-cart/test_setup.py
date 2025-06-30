"""
Test script to verify the shopping cart API setup
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    try:
        print("Testing imports...")
        
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} imported successfully")
        
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__} imported successfully")
        
        import uvicorn
        print(f"✅ Uvicorn imported successfully")
        
        import database
        print("✅ Database module imported successfully")
        
        import models
        print("✅ Models module imported successfully")
        
        import schemas
        print("✅ Schemas module imported successfully")
        
        import crud
        print("✅ CRUD module imported successfully")
        
        import api
        print("✅ API module imported successfully")
        
        import main
        print("✅ Main FastAPI app imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database creation"""
    try:
        print("\nTesting database...")
        from database import engine, Base
        from models import Product, CartItem
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_sample_data():
    """Test if sample data exists"""
    try:
        print("\nTesting sample data...")
        from database import SessionLocal
        from models import Product
        
        db = SessionLocal()
        product_count = db.query(Product).count()
        db.close()
        
        print(f"✅ Found {product_count} products in database")
        return True
        
    except Exception as e:
        print(f"❌ Sample data error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚗 Automobile Parts Shopping Cart API - Setup Verification")
    print("=" * 60)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_database():
        all_passed = False
    
    if not test_sample_data():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your setup is working correctly.")
        print("\nNext steps:")
        print("1. Start the server: .venv\\Scripts\\python.exe -m uvicorn main:app --reload")
        print("2. Open your browser to: http://localhost:8000/docs")
        print("3. Import postman_collection.json into Postman for testing")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
