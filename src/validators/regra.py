from fastapi import Request
from pydantic import BaseModel


class RegraSchema(BaseModel):
    class Produto(BaseModel):
        categoria_id: int
        produto_id: int

    produtos: list[Produto]


async def regra_validate_schema(request: Request):
    request_body = await request.body()
    RegraSchema.parse_raw(request_body)
