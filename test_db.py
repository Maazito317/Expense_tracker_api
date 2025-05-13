# test_db.py

from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models import Base, User, Expense
from sqlalchemy.exc import SQLAlchemyError


def test_connection_and_models():
    try:
        # 1) Create all tables defined on Base.metadata
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created (or already exist).")

        # 2) Open a session and do a simple query
        db = SessionLocal()
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            print("✅ Connection test passed: SELECT 1 returned 1")
        else:
            print("❌ Unexpected result from SELECT 1:", result)

        # 3) Insert and query a dummy User
        dummy = User(email="test@example.com", hashed_password="hashed_pw")
        db.add(dummy)
        db.commit()
        fetched = db.query(User).filter_by(email="test@example.com").first()
        if fetched:
            print("✅ ORM model test passed: User inserted and fetched:", fetched.email)
        else:
            print("❌ Could not fetch inserted User.")

        # 4) Clean up (optional)
        db.delete(fetched)
        db.commit()
        print("🧹 Cleaned up dummy records.")

    except SQLAlchemyError as e:
        print("❌ SQLAlchemy error:", e)
    finally:
        db.close()


if __name__ == "__main__":
    test_connection_and_models()
