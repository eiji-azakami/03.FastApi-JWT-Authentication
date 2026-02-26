# FastAPI JWT Authentication Sample

## 概要
FastAPI JWT認証 サンプル

- ユーザー認証を行い、アクセストークンを発行します。
- パスワードは72バイト以内でご利用ください。（bcrypt の制限）
- ログ出力は左記を利用 [01.FastApi-Logging](https://github.com/eiji-azakami/01.FastApi-Logging)
- テスト付き（pytest）

## Demo
Cloud Run サーバーレス構成サンプル<br>
https://fastapijwtauthentication-347911280466.asia-northeast1.run.app/docs

## 設定
.env.example に従って、.env を作成してください。

## 環境セットアップ
pythonコマンドは環境によって「python3」だったり、「python」、「py」だったりするようです。<br>
お使いの環境に合わせてコマンドを変更してください。

1. 仮想環境を作成します。

```bash
python3 -m venv venv
```

2. 仮想環境を有効化します。

```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

3. 必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

4. pipを最新バージョンにアップグレードすることを推奨します。

```bash
python -m pip install --upgrade pip
```

## 起動方法

```bash
uvicorn app.main:app --reload --no-access-log
```

## 起動後
- Swagger UI: http://127.0.0.1:8000/docs
- Redoc:        http://127.0.0.1:8000/redoc

- 仮のユーザーデータベースは下記ユーザーで動作を確認できます。
-   username = testuser、password = secret

## テスト

```bash
python -m pytest
```

# Note

確認用に認証ユーザーの情報を返却するAPIを用意しています。<br>
api/auth.py に仮のユーザーデータベースを定義しています。利用の際は適宜変更してください。<br>
<br>
テストコードは現状未実装です。後で作成します。

# Author
 
* 作成者 阿座上 英治
* 所属 　株式会社Ｌ．Ｓ．Ｅ
 
## 📝 License

MIT License  
Copyright (c) 2026 L.S.E Eiji.Azakami

This project is licensed under the MIT License.  
See the [LICENSE](https://en.wikipedia.org/wiki/MIT_License) file for details.
