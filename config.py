import typing

import yaml
from pydantic import BaseModel, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    dbms: str
    driver: str
    host: str
    port: int
    user: str
    password: str | None = None
    database: str
    debug: bool = False

    def get_url(self) -> PostgresDsn:
        return PostgresDsn(
            f'{self.dbms}+'
            f'{self.driver}://'
            f'{self.user}:'
            f'{self.password or ""}@'
            f'{self.host}:'
            f'{self.port}/'
            f'{self.database}'
        )


class AuthenticationSettings(BaseModel):
    enabled: bool
    api_key: SecretStr


class Settings(BaseSettings):
    database: DatabaseSettings
    authentication: AuthenticationSettings

    @classmethod
    def from_yaml(cls, file_path: str) -> typing.Self:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        return cls(**data)


settings = Settings.from_yaml('config.yaml')
