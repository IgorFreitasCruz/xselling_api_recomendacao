from fastapi import Request
from fastapi.responses import JSONResponse

from src.errors.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.regra_list_composer import regra_list_composer
from src.validators.regra import regra_validate_schema


async def regras_list(request: Request):
    try:
        await regra_validate_schema(request)
        http_response = await request_adapter(request, regra_list_composer())
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)


# PYDANTIC
# Produtos=[Produto(IDCategoria=3, IDProduto=0), Produto(IDCategoria=3, IDProduto=0), Produto(IDCategoria=4, IDProduto=0), Produto(IDCategoria=4, IDProduto=0)]

# await request.json()
# {'Produtos': [{'IDCategoria': 3, 'IDProduto': 0}, {'IDCategoria': 3, 'IDProduto': 0}, {'IDCategoria': 4, 'IDProduto': 0}, {'IDCategoria': 4, 'IDProduto': 0}]}
