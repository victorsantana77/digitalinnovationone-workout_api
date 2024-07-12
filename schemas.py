from pydantic import BaseModel

class AtletaBase(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str
    saldo: float

class AtletaCreate(AtletaBase):
    pass

class Atleta(AtletaBase):
    id: int

    class Config:
        orm_mode = True