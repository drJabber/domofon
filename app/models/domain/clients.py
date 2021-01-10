from typing import Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security


class Client(RWModel):
    client_id: str


class ClientInDB(IDModelMixin, DateTimeModelMixin, Client):
    salt: str = ""
    hashed_secret: str = ""

    def check_secret(self, secret: str) -> bool:
        return security.verify_password(self.salt + secret, self.hashed_secret)

    def change_secret(self, secret: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_secret = security.get_password_hash(self.salt + secret)
