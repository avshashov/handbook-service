from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DatabaseSettings, settings


class DBConnection:
    def __init__(self, db_settings: DatabaseSettings) -> None:
        self._settings = db_settings
        self.engine = create_async_engine(
            url=db_settings.get_url().encoded_string(),
            echo=db_settings.debug,
            pool_size=db_settings.pool_size,
            max_overflow=db_settings.max_overflow,
            pool_timeout=60,
        )
        self.async_session = async_sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session


database = DBConnection(db_settings=settings.database)
