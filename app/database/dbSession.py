from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Generator
from app.utils.logger import get_logger
from app.exception_handlers import DatabaseException
import os

load_dotenv()
logger = get_logger()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error: {e}")
        raise DatabaseException("Database operation failed") from e
    finally:
        try:
            db.close()
            logger.debug("Database session closed")
        except Exception as e:
            logger.warning(f"Error closing DB session: {e}")


@contextmanager
def safe_commit_transaction(db):
    try:
        yield
        db.commit()
        logger.debug("Transaction committed successfully")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Transaction error: {e}")
        raise DatabaseException("Transaction failed and was rolled back") from e
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in transaction: {e}")
        raise DatabaseException("Unexpected error during transaction") from e
