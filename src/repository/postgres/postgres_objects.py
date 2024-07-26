"""Module for the Postgres database"""
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=True)
    nome: str
    descricao: str
    sku: str
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    dt_alteracao: datetime = None
    ativo: bool = True

    # categoria_id: Optional[int] = Field(foreign_key='category.id')
