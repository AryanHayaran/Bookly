# from sqlmodel import SQLModel
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from src.config import Config

# # ✅ Correct async database URL with asyncpg
# DATABASE_URL = (
#     f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASSWORD}"
#     f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
# )

# # ✅ Correct async engine creation
# async_engine = create_async_engine(
#     DATABASE_URL,
#     # echo=False,  # Set to True for SQL logs
# )

# # ✅ Initialize database (e.g., on app startup)
# async def init_db():
#     async with async_engine.begin() as conn:
#         from src.db.models import Book  # Import your models here
#         await conn.run_sync(SQLModel.metadata.create_all)

# # ✅ Dependency to get session
# async def get_session() -> AsyncSession:
#     async_session = sessionmaker(
#         async_engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#     )
#     async with async_session() as session:
#         yield session


from sqlmodel import SQLModel, text, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


async_engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    # echo=True
))


async def init_db():
    async with async_engine.begin() as conn:
        from src.db.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with Session() as session:
        yield session
