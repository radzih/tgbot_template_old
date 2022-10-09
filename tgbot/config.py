from dataclasses import dataclass

from environs import Env

from sqlalchemy.engine.url import URL


@dataclass
class DbConfig:
    name: str

    def construct_sqlalchemy_url(self, async_lib: str = 'aiosqlite') -> str:
        url = URL.create(
            drivername=f'sqlite+{async_lib}',
            database=self.name,
        )
        return str(url)

    @property
    def sqlalchemy_sync_url(self) -> str:
        url = URL.create(
            drivername='sqlite',
            database=self.name,
        )
        return str(url)


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    commands: dict[str, str]


@dataclass
class Miscellaneous:
    other_params: str | None = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS'))),
            use_redis=env.bool('USE_REDIS'),
            commands=env.json('COMMANDS'),
        ),
        db=DbConfig(
            name=env.str('DB_NAME'),
        ),
        misc=Miscellaneous()
    )
