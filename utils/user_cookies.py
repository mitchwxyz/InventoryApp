from fastapi import Cookie, Response
from uuid import uuid4


async def get_user(user_id: str = Cookie(None)):
    """
    Create a unique user ID if none exists
    """
    if not user_id:
        user_id = str(uuid4())
    return user_id


async def set_user(response: Response, user_id: str):
    """"
    Set user ID cookie in response
    """
    response.set_cookie(key="user_id", value=user_id, expires=14*60*60*24)
