from fastapi import HTTPException
from pydantic import BaseModel
import httpx


class LoginRequest(BaseModel):
    username: str
    password: str


AUTHORIZATION_URL = "https://login.sit.kmutt.ac.th/realms/student-project/protocol/openid-connect/auth"
TOKEN_URL = "https://login.sit.kmutt.ac.th/realms/student-project/protocol/openid-connect/token"
USERINFO_URL = "https://login.sit.kmutt.ac.th/realms/student-project/protocol/openid-connect/userinfo"
END_SESSION_URL = "https://login.sit.kmutt.ac.th/realms/student-project/protocol/openid-connect/logout"
CLIENT_ID = "auth-cp24un1"
CLIENT_SECRET = "VxpOUOr3xGx5WzrpmEiUE1GRxPaHj2yl"
REDIRECT_URI = "http://localhost/*"
SCOPE = "openid profile email"


async def get_token(username: str, password: str):
    async with httpx.AsyncClient() as client:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": username,
            "password": password,
            "grant_type": "password",
            "scope": SCOPE
        }
        response = await client.post(TOKEN_URL, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to authenticate")
        return response


async def login(request: LoginRequest):
    token_data = await get_token(request.username, request.password)
    return token_data