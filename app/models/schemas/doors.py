import datetime

from typing import Optional

from pydantic import BaseModel

from app.models.domain.doors import Door
from app.models.schemas.rwschema import RWSchema

class DoorIn(RWSchema):
    door_id: str

class DoorInCreate(DoorIn):
    ext_door_id: str
    ext_user: str
    ext_password: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    access_token_expires: Optional[datetime.datetime]


class DoorInUpdate(RWSchema):
    door_id: Optional[str]
    ext_door_id: Optional[str]
    ext_user: Optional[str]
    ext_password: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]
    access_token_expires: Optional[datetime.datetime]

class DoorInResponse(BaseModel):
    door: Door
