import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

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

if not DATABASE_URL:
    # Debug print for each component
    print(f"[DEBUG_PY] POSTGRES_PORT={DB_PORT}", flush=True)
    print("[DEBUG_PY] using fallback URL", flush=True)
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

print(f"[DEBUG_PY] FINAL DATABASE_URL={DATABASE_URL}", flush=True)
# 4) Create engine and session factory as before
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Session:
    """Yield a new Session per request and close it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
