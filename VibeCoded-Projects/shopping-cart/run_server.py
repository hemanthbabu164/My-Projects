#!/usr/bin/env python3

import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def test_imports():
    """Test all imports step by step"""
    print("🧪 Testing imports step by step...")
    
    # Test basic libraries
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except Exception as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except Exception as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except Exception as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    # Test project modules
    try:
        from database import engine, get_db
        print("✅ Database module imported successfully")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from models import Base, Product, CartItem
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        print(f"   Error details: {e}")
        return False
    
    try:
        import schemas
        print("✅ Schemas imported successfully")
    except Exception as e:
        print(f"❌ Schemas import failed: {e}")
        return False
    
    try:
        import crud
        print("✅ CRUD imported successfully")
    except Exception as e:
        print(f"❌ CRUD import failed: {e}")
        return False
    
    try:
        from api import products_router, cart_router
        print("✅ API routers imported successfully")
    except Exception as e:
        print(f"❌ API routers import failed: {e}")
        return False
    
    try:
        import main
        print("✅ Main FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        return False

def test_database():
    """Test database setup"""
    print("\n🗄️ Testing database setup...")
    try:
        from models import Base
        from database import engine
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_server():
    """Test if we can create the FastAPI app"""
    print("\n🚀 Testing FastAPI app creation...")
    try:
        import main
        app = main.app
        print("✅ FastAPI app created successfully")
        print(f"   App title: {app.title}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚗 Automobile Parts Shopping Cart - Diagnostic Test")
    print("=" * 60)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_database():
        success = False
    
    if not test_server():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\n🚀 Starting the server...")
        print("🌐 Open your browser to: http://127.0.0.1:8000/docs")
        print("🛒 Frontend available at: http://127.0.0.1:8000/frontend/index.html")
        print("\nPress Ctrl+C to stop the server\n")
        
        try:
            import uvicorn
            import main
            uvicorn.run(main.app, host="127.0.0.1", port=8000, reload=True)
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped by user")
        except Exception as e:
            print(f"\n❌ Server failed to start: {e}")
    else:
        print("❌ TESTS FAILED - Please fix the issues above")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
