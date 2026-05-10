from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from jose import (
    jwt,
    JWTError
)

from app.security import (
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)

router = APIRouter(
    tags=["Auth"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

USER = {
    "username": "admin",
    "password": "admin123"
}


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):
    credentials_exception = (
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={
                "WWW-Authenticate":
                "Bearer"
            }
        )
    )

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
            raise credentials_exception

        return username

    except JWTError:
        raise credentials_exception


@router.post("/login")
def login(
    form_data:
    OAuth2PasswordRequestForm =
    Depends()
):

    if (
        form_data.username
        != USER["username"]
        or form_data.password
        != USER["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    access_token = (
        create_access_token(
            {
                "sub":
                form_data.username
            }
        )
    )

    return {
        "access_token":
        access_token,
        "token_type":
        "bearer"
    }