import time

from sqlalchemy import (
    create_engine
)

from sqlalchemy.exc import (
    OperationalError
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

DATABASE_URL = (
    "mysql+pymysql://"
    "admin:admin123"
    "@mysql:3306/"
    "api_clientes"
)

MAX_RETRIES = 30
RETRY_DELAY = 2

engine = None


for attempt in range(
    MAX_RETRIES
):
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )

        connection = (
            engine.connect()
        )

        connection.close()

        print(
            "MySQL ligado!"
        )

        break

    except OperationalError:

        print(
            f"MySQL não "
            f"está pronto "
            f"({attempt + 1}/"
            f"{MAX_RETRIES})"
        )

        time.sleep(
            RETRY_DELAY
        )


if engine is None:
    raise Exception(
        "Não foi possível "
        "ligar ao MySQL."
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()