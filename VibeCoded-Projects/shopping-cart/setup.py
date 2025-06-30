"""
Setup script for the Automobile Parts Shopping Cart API

This script sets up the development environment and runs the application.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_database():
    """Initialize the database with sample data"""
    print("Initializing database...")
    from database import engine
    from models import Base
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def run_tests():
    """Run the test suite"""
    print("Running tests...")
    subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])

def start_server():
    """Start the FastAPI development server"""
    print("Starting the development server...")
    print("The API will be available at:")
    print("  - API: http://localhost:8000")
    print("  - Documentation: http://localhost:8000/docs")
    print("  - Alternative docs: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    
    subprocess.call([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    print("🚗 Automobile Parts Shopping Cart API Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "install":
            install_requirements()
        elif command == "test":
            run_tests()
        elif command == "start" or command == "run":
            start_server()
        elif command == "setup":
            install_requirements()
            create_database()
            print("\n✅ Setup complete! Run 'python setup.py start' to launch the server.")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: install, test, start, setup")
    else:
        print("Available commands:")
        print("  python setup.py install  - Install dependencies")
        print("  python setup.py setup    - Full setup (install + database)")
        print("  python setup.py test     - Run tests")
        print("  python setup.py start    - Start the development server")
        print("\nQuick start: python setup.py setup && python setup.py start")
