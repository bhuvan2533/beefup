from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.utils.logger import get_logger
import os
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

logger = get_logger()

def get_db():
    db = None
    try:
        db = SessionLocal() 
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {e}")
        raise Exception("Database connection or transaction error occurred") from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise Exception("An unexpected error occurred") from e
    finally:
        if db:
            try:
                db.close()
            except Exception as e:
                logger.warning(f"Error closing the database session: {e}")



@contextmanager
def safe_commit_transaction(db):
    try:
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Transaction error: {e}")
        db.rollback()
        raise Exception("Transaction error occurred") from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        db.rollback()
        raise Exception("An unexpected error occurred") from e
    finally:
        db.close()
        logger.info("Database session closed")
