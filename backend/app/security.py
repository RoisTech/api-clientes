from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def create_access_token(
    data: dict
):
    expire = (
        datetime.utcnow()
        + timedelta(hours=1)
    )

    to_encode = data.copy()
    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get(
            "sub"
        )

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )