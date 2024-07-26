import jwt

from src.errors.types.token_expired_error import ExpiredTokenError
from src.errors.types.token_invalid_error import TokenInvalidError
from src.presentation.http_types.http_request import HttpRequest


class AuthTokenPlugin:
    SECRET = '1234'
    ALGORITHM = 'HS256'

    def __init__(self, jwt: jwt) -> None:
        self.jwt = jwt

    def decode_jwt(self, data: str) -> dict:
        return self.jwt.decode(data, self.SECRET, self.ALGORITHM)

    def validate_token(self, http_request: HttpRequest):
        try:
            token = http_request.headers
            return self.decode_jwt(token['Authorization'])
        except self.jwt.ExpiredSignatureError:
            raise ExpiredTokenError('Token expirado')
        except self.jwt.InvalidTokenError:
            raise TokenInvalidError('Token inválido')


auth_token = AuthTokenPlugin(jwt)
