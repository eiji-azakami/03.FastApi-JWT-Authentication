"""
JWT認証を提供するAPI。

- サンプルコードです。
- 環境変数から設定値を取得し処理します。

エンドポイント:
- POST `/token`: ユーザー認証を行い、アクセストークンを発行します。
- GET `/users/me`: 現在の認証ユーザーの情報を取得します

"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 設定取得
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# パスワードをハッシュ化
# パスワードをハッシュ化して保存する際に使用します。
def get_password_hash(password):
    # bcryptは72バイトを超えるパスワードをサポートしないため制限
    password = password[:72]
    print(f"Debug: Truncated password for hashing: {password}")
    return pwd_context.hash(password)


# パスワードを検証
# 平文のパスワードとハッシュ化されたパスワードを比較します。
def verify_password(plain_password, hashed_password):
    # bcryptは72バイトを超えるパスワードをサポートしないため制限
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)


# 仮のユーザーデータベース
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": "$2b$12$3Qp/DHlwQQFJe/jrKe3E9eEz/twGhPyIHqEZH.DjpbDE0foXb79.6",  # 事前にハッシュ化されたパスワード 'secret'
        "disabled": False,
    }
}


# ユーザー情報を取得
# ユーザー名をキーにして、データベースからユーザー情報を取得します。
def get_user(db, username: str):
    user = db.get(username)
    if user:
        return user


# ユーザー認証
# ユーザー名とパスワードを検証し、正しい場合はユーザー情報を返します。
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


# アクセストークンを生成
# トークンに含めるデータと有効期限を指定してJWTトークンを生成します。
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 現在のユーザーを取得
# トークンをデコードしてユーザー情報を取得します。
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = get_user(fake_users_db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# アクティブなユーザーを取得
# ユーザーが無効化されていないかを確認します。
def get_current_active_user(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


router = APIRouter(tags=["auth"])


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # ユーザー認証を行い、アクセストークンを発行します。
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        # 認証失敗時には401エラーを返します。
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # アクセストークンの有効期限を設定します。
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # トークンを生成します。
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    # トークンとそのタイプを返します。
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: Annotated[dict, Depends(get_current_active_user)]):
    # 現在の認証ユーザーの情報を取得します。
    # hashed_passwordは除外
    user_data = {key: value for key, value in current_user.items() if key != "hashed_password"}
    return user_data
