
import json
from fastapi import status
from app.models.schemas.tokens import TokenInResponse
from app.models.domain.doors import DoorInDB
from app.core import config
from aiohttp import TCPConnector, ClientSession
import jwt

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
    login returns auth or none
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
                door.access_token = auth["access"]
                door.refresh_token = auth["refresh"]
                door.access_token_expires = auth["exp"]
                return auth
        except Exception as ex:
            pass

    """
    refresh returns auth or none
    """
    async def refresh(door: DoorInDB):
        try:
            session = ClientSession(connector=TCPConnector(ssl=False))
            headers = Utils.get_headers()
            data = {"refresh": door.refresh_token}
            async with session.post(config.UFANET_SERVICE_URL+config.UFANET_REFRESH_TOKEN_API, \
                            data=json.dumps(data), \
                            headers=headers) as response:
                auth = await response.json()
                door.access_token = auth["access"]
                door.refresh_token = auth["refresh"]
                door.access_token_expires = auth["exp"]
                return auth
        except Exception as ex:
            pass


    """
      returns true or false
      updates door by tokens
    """
    async def open(self, door: DoorInDB, refresh: bool = False) -> bool:
        auth = None
        if not door.access_token:
            auth = await self.login(door)

        if auth:
            headers=Utils.get_headers().copy()
            headers["Authorization"]=auth["access"]
            session = ClientSession(connector=TCPConnector(ssl=False))
            async with session.post(config.UFANET_SERVICE_URL+config.UFANET_OPEN_API, headers=headers) as response:
                result=await response.status()

            if result==status.HTTP_401_UNAUTHORIZED and not refresh:
                auth = await self.refresh_token(door)
                if auth:
                    return await self.open(door, True)

            return result==status.HTTP_200_OK

        return False