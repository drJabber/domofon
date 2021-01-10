
import json

from app.models.schemas.tokens import TokenInResponse
from app.models.domain.doors import DoorInDB
from app.core import config
from aiohttp import TCPConnector, ClientSession

class Utils:
    @staticmethod
    def get_headers():
        return {
            "User-Agent": "android/2.1.10/Samsung",
            "Content-Type": "application/json",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

class Domofon:
    def __init__(self):
        pass

    """
    returns auth or none
    """
    async def login(door: DoorInDB):
        try:
            session = ClientSession(connector=TCPConnector(ssl=False))
            headers = Utils.get_headers()
            data = {"contract": door.ext_user, "password": door.ext_password}
            async with session.post(config.UFANET_SERVICE_URL+config.UFANET_LOGIN_API, \
                            data=json.dumps(data), \
                            headers=headers) as response:
                auth = await response.json()
                return auth
        except Exception as ex:
            pass



    async def open(self, door: DoorInDB) -> bool:
        auth = await self.login(door)
        if auth:

            return True
            
        return False