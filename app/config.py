from datetime import timedelta
from pathlib import Path
from typing import Any, Optional, Union

from pydantic import (
    BaseSettings,
    Field,
    PostgresDsn,
    validator,
)

from .util import normalize_postgres_dsn_for_atoti_sql


class Config(BaseSettings):
    """Hold all the configuration properties of the app, not only the ones related to atoti.

    See https://pydantic-docs.helpmanual.io/usage/settings/.
    """

    data_refresh_period: Optional[timedelta] = timedelta(minutes=1)

    # The $PORT environment variable is used by most PaaS to indicate the port the app server should bind to.
    port: int = 9090

    aws_s3_path = "s3://data.atoti.io/notebooks/french-presidential-election-2022/"

    user_content_storage: Optional[Union[PostgresDsn, Path]] = Field(
        default=Path("content"),
        # $DATABASE_URL is used by some PaaS such to designate the URL of the app's primary database.
        # For instance: https://devcenter.heroku.com/articles/heroku-postgresql#designating-a-primary-database.
        env="database_url",
    )

    @validator("user_content_storage")
    @classmethod
    def normalize_postgresql_dsn(cls, value: Union[PostgresDsn, Any]) -> Any:
        return (
            normalize_postgres_dsn_for_atoti_sql(value)
            if isinstance(value, PostgresDsn)
            else value
        )
