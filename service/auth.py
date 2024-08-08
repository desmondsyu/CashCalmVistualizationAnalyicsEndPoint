import hashlib
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import service.Connector as Connector


# Hash password function
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# Security scheme
security = HTTPBasic()


def auth_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_email = credentials.username
    current_password_sha256 = hash_password(credentials.password)
    query = f"SELECT user_id from user WHERE email = '{current_email}' and PASSWORD = '{current_password_sha256}'"
    connector = Connector.Connector()
    result = connector.execute(query)

    if result is None or result == []:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def auth_get_username_id(credentials: Annotated[HTTPBasicCredentials, Depends(security)],):
    email = credentials.username
    pw = hash_password(credentials.password)

    query = f"SELECT user_id,username FROM user WHERE email = '{email}' and password = '{pw}'"

    connection = Connector.Connector()
    result = connection.execute(query)
    if result is None or result == []:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User not found"
        )

    else:
        return result