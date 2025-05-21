from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres.connection import database

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
