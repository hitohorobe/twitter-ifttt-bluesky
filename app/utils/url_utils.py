import re
from urllib.parse import urljoin, urlparse

import requests

from app.models.bluesky_models import LabelEnum
from app.settings.bluesky_settings import BLUESKY_REQUEST_TIMEOUT
from app.settings.expandable_url_list import EXPANDABLE_HOSTS, TWITTER_INTERNAL_HOSTS
from app.utils.ogp_utils import get_ogp


def extract_url(text: str) -> list[str]:
    """入力した文字列の中からURLを全て抜粋してリストで返す"""
    urls = []
    for url in re.findall(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", text):
        urls.append(url)
    return urls


def expand_url(url: str) -> str:
    """入力したURLを展開して返す。URLのホストによって次の挙動をする
    - ホストが t.co でも Twitter/X の内部ドメイン(TWITTER_INTERNAL_HOSTS)でもない場合:
      リクエストを送らずそのまま返す
      (アフィリエイトリンク等、展開すると最終URLに正規化されアフィリエイトが
      機能しなくなるURLを保護するため)
    - ホストが t.co の場合:
      1回リダイレクトを辿り、その結果のURLを返す。
      ただし、リダイレクト先が Twitter/X の内部ドメインだった場合は、
      リダイレクトが発生しなくなるまで再帰的に展開を続ける
    - ホストが Twitter/X の内部ドメインの場合:
      リダイレクトが発生しなくなるまで再帰的に展開する。
      最終的なURLの末尾に /photo/1 を含む場合は、それを取り除いて返す
    """
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
    headers = {"User-Agent": user_agent}
    try:
        hostname = urlparse(url).hostname
        if hostname not in EXPANDABLE_HOSTS:
            return url

        response = requests.get(
            url, timeout=BLUESKY_REQUEST_TIMEOUT, headers=headers, allow_redirects=False
        )
        if 300 <= response.status_code < 400:
            location = urljoin(url, response.headers["Location"])
            return expand_url(location)
        else:
            if hostname in TWITTER_INTERNAL_HOSTS and "/photo/1" in url:
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
