import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    import fastapi
    print(f"✅ FastAPI {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI import error: {e}")

try:
    import uvicorn
    print("✅ Uvicorn imported")
except ImportError as e:
    print(f"❌ Uvicorn import error: {e}")

try:
    import sqlalchemy
    print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
except ImportError as e:
    print(f"❌ SQLAlchemy import error: {e}")

print("\nTesting project modules...")

try:
    import database
    print("✅ database.py imported")
except Exception as e:
    print(f"❌ database.py error: {e}")

try:
    import models
    print("✅ models imported")
except Exception as e:
    print(f"❌ models error: {e}")

try:
    import main
    print("✅ main.py imported")
    print("✅ FastAPI app created successfully!")
except Exception as e:
    print(f"❌ main.py error: {e}")

print("\nAttempting to start server...")
if 'main' in locals():
    try:
        import uvicorn
        print("Starting server on http://127.0.0.1:8000")
        print("Open your browser to: http://127.0.0.1:8000/docs")
        uvicorn.run(main.app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"❌ Server start error: {e}")
else:
    print("❌ Cannot start server - main module failed to import")
