from __future__ import annotations
import auth.models
import os
import sqlalchemy
import sqlalchemy.orm


class Database:
    __connection: Database = None

    def __init__(self):
        self._engine = None
        self._live_session = None

    def __enter__(self):
        self._live_session = self.session()
        return self._live_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._live_session.close()

    @property
    def engine(self) -> sqlalchemy.engine.Engine:
        return self._engine

    def build(self):
        auth.models.BaseModel.metadata.create_all(self.engine)

    def connect(self):
        user = os.environ.get("DB_USER", "user_service")
        database = os.environ.get("DB_USER", "user_service")
        host = os.environ.get("DB_HOST", "0.0.0.0")
        port = os.environ.get("DB_PORT", "5432")
        sslmode = "require" if os.environ.get("PRODUCTION", False) else None
        password = os.environ.get("DB_PASSWORD", "dev-env-password-safe-to-be-public")

        self._engine = sqlalchemy.create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{database}",
            connect_args={
                "sslmode": sslmode
            }
        )

        self.build()

    def session(self) -> sqlalchemy.orm.Session:
        return sqlalchemy.orm.Session(bind=self.engine)

    @classmethod
    def get_connection(cls, database: Database = None) -> Database:
        if database:
            return database

        if not cls.__connection:
            cls.__connection = cls()
            cls.__connection.connect()
        return cls.__connection
