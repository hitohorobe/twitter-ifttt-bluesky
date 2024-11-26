import re

import requests

from app.models.bluesky_models import LabelEnum
from app.settings.bluesky_settings import BLUESKY_REQUEST_TIMEOUT
from app.utils.ogp_utils import get_ogp


def extract_url(text: str) -> list[str]:
    """入力した文字列の中からURLを全て抜粋してリストで返す"""
    urls = []
    for url in re.findall(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", text):
        urls.append(url)
    return urls


def expand_url(url: str) -> str:
    """入力したURLを展開して返す。OGPの有無によって、次の挙動をする
    - amzn.to: そのまま返す
    - bit.ly: そのまま返す
    - twitter.com または x.com で末尾に/photo/1を含む場合: 末尾の/photo/1を削除して返す
    - それ以外: 展開が完了するまで再帰的に処理し、展開後のURLを返す
    """
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
    headers = {"User-Agent": user_agent}
    try:
        if "https://amzn.to" in url:
            return url
        if "https://bit.ly" in url:
            return url
        response = requests.get(
            url, timeout=BLUESKY_REQUEST_TIMEOUT, headers=headers, allow_redirects=False
        )
        if 300 <= response.status_code < 400:
            return expand_url(response.headers["Location"])
        else:
            if "twitter.com" in url or "x.com" in url:
                if "/photo/1" in url:
                    return url.replace("/photo/1", "")
            return response.url
    except Exception as e:
        print(e)
        return url


def ommit_long_url(url: str, length=32) -> str:
    """入力したURL文字列のうち先頭29文字と末尾に...をつけた32文字を返す。
    ただし、入力した文字列が32文字以下の場合はそのまま返す
    """
    if len(url) > length:
        return url[: length - 3] + "..."
    return url


def extract_hashtags(text: str) -> list[str]:
    """入力した文字列の中からハッシュタグを全て抜粋してリストで返す
    ただし、url anchor(文中に#がついているもの)は除外する
    """
    hashtags = []
    # urlを全て除外
    for url in extract_url(text):
        text = text.replace(url, "")
    for hashtag in re.findall(r"#\S+", text):
        hashtags.append(hashtag)
    return hashtags


def get_byte_length(text: str) -> int:
    """入力した文字列のバイト長を返す"""
    return len(text.encode("utf-8"))
