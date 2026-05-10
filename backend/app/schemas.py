from pydantic import BaseModel


class ClienteBase(BaseModel):
    nome: str
    email: str
    telefone: str
    morada: str
    nif: str


class ClienteCreate(
    ClienteBase
):
    pass


class ClienteResponse(
    ClienteBase
):
    id: int

    class Config:
        from_attributes = True