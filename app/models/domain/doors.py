from typing import Optional
import datetime
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class Door(RWModel):
    door_id: str

class DoorInDB(IDModelMixin, DateTimeModelMixin, Door):
    ext_door_id: str
    ext_user: str
    ext_password: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    access_token_expires: Optional[datetime.datetime]
