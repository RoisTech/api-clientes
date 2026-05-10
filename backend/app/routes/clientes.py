from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import (
    Session
)

from app.database import (
    get_db
)

from app.models import (
    Cliente
)

from app.schemas import (
    ClienteCreate
)

from app.routes.auth import (
    get_current_user
)

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.post("/")
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(
        get_db
    ),
    current_user=Depends(
        get_current_user
    )
):
    novo_cliente = (
        Cliente(
            **cliente.dict()
        )
    )

    db.add(
        novo_cliente
    )

    db.commit()

    db.refresh(
        novo_cliente
    )

    return novo_cliente


@router.get("/")
def listar_clientes(
    db: Session = Depends(
        get_db
    ),
    current_user=Depends(
        get_current_user
    )
):
    return (
        db.query(
            Cliente
        ).all()
    )


@router.get("/{cliente_id}")
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(
        get_db
    ),
    current_user=Depends(
        get_current_user
    )
):

    cliente = (
        db.query(
            Cliente
        )
        .filter(
            Cliente.id == cliente_id
        )
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return cliente


@router.put("/{cliente_id}")
def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteCreate,
    db: Session = Depends(
        get_db
    ),
    current_user=Depends(
        get_current_user
    )
):

    cliente_db = (
        db.query(
            Cliente
        )
        .filter(
            Cliente.id == cliente_id
        )
        .first()
    )

    if not cliente_db:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    cliente_db.nome = cliente.nome
    cliente_db.email = cliente.email
    cliente_db.telefone = cliente.telefone
    cliente_db.morada = cliente.morada
    cliente_db.nif = cliente.nif

    db.commit()
    db.refresh(
        cliente_db
    )

    return cliente_db


@router.delete("/{cliente_id}")
def apagar_cliente(
    cliente_id: int,
    db: Session = Depends(
        get_db
    ),
    current_user=Depends(
        get_current_user
    )
):

    cliente = (
        db.query(
            Cliente
        )
        .filter(
            Cliente.id == cliente_id
        )
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    db.delete(
        cliente
    )

    db.commit()

    return {
        "mensagem":
        "Cliente removido com sucesso"
    }