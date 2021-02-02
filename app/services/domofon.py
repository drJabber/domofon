
import json
import datetime
from fastapi import status
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
    login returns auth or none
    """
    async def login(self, door: DoorInDB):
        try:
            headers = Utils.get_headers()
            data = {"contract": door.ext_user, "password": door.ext_password}
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.post(config.UFANET_SERVICE_URL+config.UFANET_LOGIN_API, \
                                data=json.dumps(data), \
                                headers=headers) as response:
                    auth = await response.json()
                    door.access_token = auth["token"]["access"]
                    door.refresh_token = auth["token"]["refresh"]
                    door.access_token_expires = datetime.datetime.fromtimestamp(auth["token"]["exp"])
                    return auth
        except Exception as ex:
            pass

    """
    refresh returns auth or none
    """
    async def refresh(self, door: DoorInDB):
        try:
            headers = Utils.get_headers()
            data = {"refresh": door.refresh_token}
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.post(config.UFANET_SERVICE_URL+config.UFANET_REFRESH_TOKEN_API, \
                                data=json.dumps(data), \
                                headers=headers) as response:
                    auth = await response.json()
                    door.access_token = auth["access"]
                    door.refresh_token = auth["refresh"]
                    door.access_token_expires = datetime.datetime.fortimestamp(auth["exp"])
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

        if door.access_token:
            try:
                headers=Utils.get_headers().copy()
                headers["Authorization"]="jwt "+door.access_token
                result=status.HTTP_400_BAD_REQUEST
                async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                    async with session.get(config.UFANET_SERVICE_URL+config.UFANET_SKUD_API, headers=headers) as response:
                        result=response.status
                        if result==status.HTTP_200_OK:
                            skud=await response.json()
                            door.ext_door_id=skud[0]["id"]
                            url=config.UFANET_SERVICE_URL+config.UFANET_SKUD_API+str(door.ext_door_id)+"/open/"
                            async with session.get(url, headers=headers) as response:
                                result=response.status
                                op_result=await response.json()


                if result==status.HTTP_401_UNAUTHORIZED and not refresh:
                    auth = await self.refresh(door)
                    if auth:
                        return await self.open(door, True)
                if result==status.HTTP_403_FORBIDDEN:
                    auth = await self.login(door)
                    if auth:
                        return await self.open(door, True)
                
                return result==status.HTTP_200_OK
            except:
                return False

        return False