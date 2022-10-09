from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tgbot.config import DbConfig


def create_session_pool(
    db: DbConfig,
    echo=False,
) -> sessionmaker:
    async_engine = create_async_engine(
        db.construct_sqlalchemy_url(),
        future=True,
        echo=echo,
    )

    session_pool = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession
        )
    return session_pool
