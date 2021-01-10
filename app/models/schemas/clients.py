from typing import Optional

from pydantic import BaseModel

from app.models.domain.clients import Client
from app.models.schemas.rwschema import RWSchema


class ClientInLogin(RWSchema):
    client_id: str
    client_secret: str


class ClientInCreate(ClientInLogin):
    client_id: str


class ClientInUpdate(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class ClientWithToken(Client):
    token: str


class ClientInResponse(RWSchema):
    client: ClientWithToken

# class ClientRefreshParams(RWSchema):

