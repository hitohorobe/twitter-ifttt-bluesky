# twitter-ifttt-bluesky
Twitter のPOST を IFTTT 経由で取得し、BlueskyにクロスポストするためのAPIサーバです


## エンドポイントの仕様
- POST `/twitter_to_bluesky`

## 環境構築構築
### 環境変数の設定
`cp .env.sample .env`
`pytest`を実行するためにテスト用アカウントを用意し、`TEST_HANDLE`にハンドル(例 @hitohorobe.bsky.social), `TEST_APP_PASSWORD`にアプリパスワードを設定する

### コンテナのビルド
`make up`

### 実行
`make up`

### API Mockの確認
- swagger [http://localhost:8000/docs](http://localhost:8000/docs)
- redoc [http://localhost:8000/redoc](http://localhost:8000/redoc)
