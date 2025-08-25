from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

ASYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SYNC_SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)
engine = create_engine(SYNC_SQLALCHEMY_DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def async_get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Define a dependency that will be used to get a database session.


def get_db():
    db = SessionLocal()  # create a new session
    try:
        yield db  # yield the session to be used in the route handlers
    finally:
        db.close()  # close the session after use
