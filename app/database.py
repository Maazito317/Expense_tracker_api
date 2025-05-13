import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1) Load .env file from project root
load_dotenv()

# 2) Read individual values (as defined in your .env)
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# 3) Construct the full URL dynamically
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 4) Create engine and session factory as before
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # Wrapped in text()
        print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection failed:", e)
    finally:
        db.close()


test_connection()
