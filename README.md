# twitter-ifttt-bluesky
Twitter のPOST を IFTTT 経由で取得し、BlueskyにクロスポストするためのAPIサーバです  

## エンドポイントの仕様
- POST `https://twitter-ifttt-bluesky.hito-horobe.net/twitter_to_bluesky`
- ペイロード
```
{
    "handle": "<Blueskyのハンドル>",
    "app_password": "<Blueskyのアプリパスワード>",
    "text": "<ツイートの本文>",
    "link_to_tweet": "<元ツイートへのリンク>"

}
```

## 環境構築
### 環境変数の設定
- `pytest`を実行するためにテスト用アカウントを用意する
- `cp .env.sample .env`
- `.env`にて、`TEST_HANDLE`にハンドル(例 @hitohorobe.bsky.social), `TEST_APP_PASSWORD`にアプリパスワードを設定する

### コンテナのビルド
`make build`

### 実行
`make up`

### ローカルでのAPI Mockの確認
- swagger [http://localhost:8080/docs](http://localhost:8080/docs)
- redoc [http://localhost:8080/redoc](http://localhost:8080/redoc)


## デプロイ
- mainブランチが更新されると`cloudrun`へ自動でデプロイ
