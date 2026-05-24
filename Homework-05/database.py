from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# FIXME: переделать на env переменную перед деплоем
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
