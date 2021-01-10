from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Form

from app.api.dependencies.database import get_repository
from app.core import config
from app.db.errors import EntityDoesNotExist
from app.db.repositories.clients import ClientsRepository
from app.db.repositories.users import UsersRepository
from app.models.schemas.tokens import Token
from app.models.schemas.users import (
    UserInCreate,
    # UserInLogin,
    UserInResponse,
    UserWithToken,
)

from app.models.schemas.clients import (
    ClientInCreate,
    ClientInLogin,
    ClientInResponse,
    ClientWithToken,
)

from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken, check_client_id_is_taken
 

router = APIRouter()

class OAuth2ClientCredentialsRequestForm:
    """
    This is a dependency class, use it like:

        @app.post("/login")
        def login(form_data: OAuth2ClientCredentialsRequestForm = Depends()):
            data = form_data.parse()
            for scope in data.scopes:
                print(scope)
            if data.client_id:
                print(data.client_id)
            if data.client_secret:
                print(data.client_secret)
            return data


    It creates the following Form request parameters in your endpoint:

    grant_type: the OAuth2 spec says it is required and MUST be the fixed string "password".
        Nevertheless, this dependency class is permissive and allows not passing it. If you want to enforce it,
        use instead the OAuth2PasswordRequestFormStrict dependency.
    scope: Optional string. Several scopes (each one a string) separated by spaces. E.g.
        "items:read items:write users:read profile openid"
    client_id: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    client_secret: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    """

    def __init__(
        self,
        grant_type: str = Form(None),
        scope: str = Form(""),
        client_id: str = Form(...),
        client_secret: str = Form(...),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret



# @router.post("/login", response_model=UserInResponse, name="auth:login")
@router.post("/token", response_model=Token, name="auth:token")
async def login(
    # user_login: UserInLogin = Body(..., embed=True, alias="user"),
    # user_login: OAuth2PasswordRequestForm = Depends(),
    client_creds: OAuth2ClientCredentialsRequestForm = Depends(),
    clients_repo: ClientsRepository = Depends(get_repository(ClientsRepository)),
    # users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> Token:
    wrong_login_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )

    try:
        # user = await users_repo.get_user_by_email(email=user_login.email)
        # user = await users_repo.get_user_by_username(username=user_login.username)
        client = await clients_repo.get_client_by_client_id(client_id=client_creds.client_id)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error
        # raise wrong_login_error from existence_error

    if not client.check_secret(client_creds.client_secret):
        raise wrong_login_error

    token = jwt.create_access_token_for_client(client, str(config.SECRET_KEY))
    refresh_token = jwt.create_refresh_token_for_client(client, str(config.SECRET_KEY))

    return Token(
        access_token=token,
        refresh_token=refresh_token,
        token_type="bearer"
    )




@router.post(
    "/register_user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:register_user",
)
async def register_user(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    if await check_username_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )

    user = await users_repo.create_user(**user_create.dict())

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
        ),
    )

@router.post(
    "/register_client",
    status_code=status.HTTP_201_CREATED,
    response_model=ClientInResponse,
    name="auth:register_client",
)
async def register_client(
    client_create: ClientInCreate = Body(..., embed=True, alias="client"),
    clients_repo: ClientsRepository = Depends(get_repository(ClientsRepository)),
) -> ClientInResponse:
    if await check_client_id_is_taken(clients_repo, client_create.client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    client = await clients_repo.create_client(**client_create.dict())

    token = jwt.create_access_token_for_client(client, str(config.SECRET_KEY))
    return ClientInResponse(
        client=ClientWithToken(
            client_id=client.client_id,
            token=token,
        ),
    )
