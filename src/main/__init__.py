from fastapi import APIRouter

from src.main.rest.recomendacao import recomendacao_list
from src.main.rest.regras import regras_list
from src.validators.recomendacao import (
    BadRequestError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    UnprocessableEntityError,
)

router = APIRouter()

router.add_api_route(
    "/regras-ia",
    endpoint=regras_list,
    methods=["POST"],
    include_in_schema=False,
)
router.add_api_route(
    "/regras-ia-recomendacao",
    endpoint=recomendacao_list,
    methods=["POST"],
    responses={
        400: {"model": BadRequestError},
        401: {"model": UnauthorizedError},
        404: {"model": NotFoundError},
        422: {"model": UnprocessableEntityError},
        500: {"model": InternalServerError},
    },
    name="Recomendação de produtos baseado em regras de IA.",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["algoritmo", "produtos_sku"],
                        "type": "object",
                        "properties": {
                            "algoritmo": {"type": "string"},
                            "produtos_sku": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    }
                }
            },
            "required": True,
        },
    },
    tags=["Recomendação de produtos"],
)


def init_app(app):
    app.include_router(router)
