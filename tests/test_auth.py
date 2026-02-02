"""
auth.py モジュールのテストスクリプト

テスト内容:
1. パスワード関連の関数のテスト
   - パスワードのハッシュ化と検証

2. ユーザー管理のテスト
   - ユーザー情報の取得と認証

3. トークン管理のテスト
   - トークンの生成とデコード

4. エンドポイントのテスト
   - /token エンドポイントでのログイン
   - /users/me エンドポイントでのユーザー情報取得

pytest を使用してテストを実行してください。
"""

from fastapi.testclient import TestClient
from app.main import app
from app.api.auth import (
    get_password_hash,
    verify_password,
    authenticate_user,
    create_access_token,
    get_user,
    fake_users_db,
)
from datetime import timedelta
from jose import jwt
import os

client = TestClient(app)

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


# パスワード関連のテスト
def test_get_password_hash():
    password = "testpassword"
    hashed = get_password_hash(password)
    # パスワードが正しくハッシュ化されているかを確認
    assert verify_password(password, hashed) is True


def test_verify_password():
    password = "testpassword"
    wrong_password = "wrongpassword"
    hashed = get_password_hash(password)
    # 正しいパスワードで検証が成功するかを確認
    assert verify_password(password, hashed) is True
    # 間違ったパスワードで検証が失敗するかを確認
    assert verify_password(wrong_password, hashed) is False


# ユーザー管理のテスト
def test_get_user():
    user = get_user(fake_users_db, "testuser")
    # ユーザーが存在する場合、正しいユーザー情報が取得できるかを確認
    assert user is not None
    # 取得したユーザーのユーザー名が正しいかを確認
    assert user["username"] == "testuser"


def test_authenticate_user():
    user = authenticate_user(fake_users_db, "testuser", "secret")
    # 正しいユーザー名とパスワードで認証が成功するかを確認
    assert user is not False
    # 認証されたユーザーのユーザー名が正しいかを確認
    assert user["username"] == "testuser"

    user = authenticate_user(fake_users_db, "wronguser", "secret")
    # 存在しないユーザー名で認証が失敗するかを確認
    assert user is False

    user = authenticate_user(fake_users_db, "testuser", "wrongpassword")
    # 間違ったパスワードで認証が失敗するかを確認
    assert user is False


# トークン管理のテスト
def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # トークンに含まれるデータが正しいかを確認
    assert decoded["sub"] == "testuser"


def test_get_current_user():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    # トークンを使用して現在のユーザー情報が正しく取得できるかを確認
    assert response.status_code == 200
    # 取得したユーザー情報に正しいユーザー名が含まれているかを確認
    assert response.json()["username"] == "testuser"


# エンドポイントのテスト
def test_login_for_access_token():
    response = client.post("/token", data={"username": "testuser", "password": "secret"})
    # 正しい認証情報でアクセストークンが発行されるかを確認
    assert response.status_code == 200
    # レスポンスにアクセストークンが含まれているかを確認
    assert "access_token" in response.json()
    # トークンタイプが"bearer"であるかを確認
    assert response.json()["token_type"] == "bearer"


def test_read_users_me():
    response = client.post("/token", data={"username": "testuser", "password": "secret"})
    token = response.json()["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    # トークンを使用して現在のユーザー情報が正しく取得できるかを確認
    assert response.status_code == 200
    # 取得したユーザー情報に正しいユーザー名が含まれているかを確認
    assert response.json()["username"] == "testuser"
