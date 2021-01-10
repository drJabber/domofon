from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security

# from fastapi.security import APIKeyHeader
from fastapi.security import OAuth2, OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

from starlette import status
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies.database import get_repository
from app.core.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.db.repositories.clients import ClientsRepository
from app.models.domain.users import User
from app.models.domain.clients import Client
from app.resources import strings
from app.services import jwt

HEADER_KEY = "Authorization"


# class RWAPIKeyHeader(APIKeyHeader):
#     async def __call__(  # noqa: WPS610
#         self,
#         request: requests.Request,
#     ) -> Optional[str]:
#         try:
#             return await super().__call__(request)
#         except StarletteHTTPException as original_auth_exc:
#             raise HTTPException(
#                 status_code=original_auth_exc.status_code,
#                 detail=strings.AUTHENTICATION_REQUIRED,
#             )

class Oauth2ClientCredentials(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=strings.NOT_AUTHENTICATED,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional

def get_current_client_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_client if required else _get_current_client_optional


# def _get_authorization_header_retriever(
#     *,
#     required: bool = True,
# ) -> Callable:  # type: ignore
#     return _get_authorization_header if required else _get_authorization_header_optional


# def _get_authorization_header(
#     api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
# ) -> str:
#     try:
#         token_prefix, token = api_key.split(" ")
#     except ValueError:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail=strings.WRONG_TOKEN_PREFIX,
#         )

#     if token_prefix != JWT_TOKEN_PREFIX:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail=strings.WRONG_TOKEN_PREFIX,
#         )

#     return token


# def _get_authorization_header_optional(
#     authorization: Optional[str] = Security(
#         RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
#     ),
# ) -> str:
#     if authorization:
#         return _get_authorization_header(authorization)

#     return ""

def _get_authorization_token_retriever(*, 
    required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_token if required else _get_authorization_token_optional


# async def _get_authorization_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/users/token"))) -> str:
async def _get_authorization_token(token: str = Depends(Oauth2ClientCredentials(tokenUrl="api/client/token"))) -> str:
    return token

# async def _get_authorization_token_optional(authorization: Optional[str] = Depends(OAuth2PasswordBearer(tokenUrl="api/users/token"))) -> str:
async def _get_authorization_token_optional(authorization: Optional[str] = Depends(Oauth2ClientCredentials(tokenUrl="api/client/token"))) -> str:
    if authorization:
        return _get_authorization_token(authorization)

    return ""

async def _get_current_user(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_authorization_token_retriever()),
    # token: str = Depends(_get_authorization_header_retriever()),
) -> User:
    try:
        username = jwt.get_username_from_token(token, str(SECRET_KEY))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )

    try:
        return await users_repo.get_user_by_username(username=username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )


async def _get_current_user_optional(
    repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_authorization_token_retriever(required=False)),
    # token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return await _get_current_user(repo, token)

    return None

async def _get_current_client(
    clients_repo: ClientsRepository = Depends(get_repository(ClientsRepository)),
    token: str = Depends(_get_authorization_token_retriever()),
    # token: str = Depends(_get_authorization_header_retriever()),
) -> Client:
    try:
        client_id = jwt.get_client_id_from_token(token, str(SECRET_KEY))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )

    try:
        return await clients_repo.get_client_by_client_id(client_id=client_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )


async def _get_current_client_optional(
    repo: ClientsRepository = Depends(get_repository(ClientsRepository)),
    token: str = Depends(_get_authorization_token_retriever(required=False)),
    # token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return await _get_current_client(repo, token)

    return None

    
    
