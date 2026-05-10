from fastapi import (
    FastAPI
)

from app.database import (
    engine,
    Base
)

from app.routes.auth import (
    router as auth_router
)

from app.routes.clientes import (
    router as clientes_router
)

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title=(
        "API Clientes"
    )
)

app.include_router(
    auth_router
)

app.include_router(
    clientes_router
)


@app.get("/")
def home():

    return {
        "mensagem":
        "API Clientes online",
        "docs":
        "http://localhost/docs"
    }