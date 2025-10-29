#!/usr/bin/env python3
"""
Database connection test script
Run this to verify your PostgreSQL connection is working
"""

import sys
from sqlalchemy import create_engine, text
from config import settings

def test_database_connection():
    """Test the database connection using credentials from .env file"""
    try:
        print("🔍 Testing database connection...")
        print(f"📊 Database URL: {settings.DATABASE_URL}")
        
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"📋 PostgreSQL version: {version}")
            
            # Test if we can create the database if it doesn't exist
            try:
                connection.execute(text("CREATE DATABASE easeops_db;"))
                print("✅ Database 'easeops_db' created successfully!")
            except Exception as e:
                if "already exists" in str(e):
                    print("✅ Database 'easeops_db' already exists!")
                else:
                    print(f"⚠️  Database creation note: {e}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your .env file has correct credentials")
        print("3. Verify the database name exists")
        print("4. Check if your user has proper permissions")
        return False

def test_application_startup():
    """Test if the FastAPI application can start with current config"""
    try:
        print("\n🚀 Testing application startup...")
        from main import app
        print("✅ FastAPI application loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Application startup failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 EaseOps E-Library - Database Connection Test")
    print("=" * 50)
    
    # Test database connection
    db_success = test_database_connection()
    
    # Test application startup
    app_success = test_application_startup()
    
    print("\n" + "=" * 50)
    if db_success and app_success:
        print("🎉 All tests passed! Your setup is ready to go!")
        print("\n📝 Next steps:")
        print("1. Run: python create_sample_data.py")
        print("2. Run: uvicorn main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
