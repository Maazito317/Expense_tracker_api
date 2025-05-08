from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, future=True, echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Add to app/db/database.py
def test_connection():
    try:
        db = session_local()
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection failed:", e)
    finally:
        db.close()


test_connection()  # Run this once to verify
