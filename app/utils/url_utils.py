import re

import requests

from app.models.bluesky_models import LabelEnum
from app.utils.ogp_utils import get_ogp


def extract_url(text: str) -> list[str]:
    """入力した文字列の中からURLを全て抜粋してリストで返す"""
    urls = []
    for url in re.findall(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", text):
        urls.append(url)
    return urls


def expand_url(url: str) -> str:
    """入力したURLを展開して返す。OGPの有無によって、次の挙動をする
    - t.coの場合: 展開して返す
    - それ以外のURLの場合
      - OGPがある場合: 入力したURLをそのまま返す
      - OGPがない場合: OGPが出現するまで、もしくはこれ以上展開できなくなるまで再起的にURLを展開し、展開先のURLを返す
    """
    try:
        if "t.co" in url:
            response = requests.head(url, timeout=10)
            return response.headers["Location"]
        ogp = get_ogp(url)
        if ogp is not None and ogp.image:
            return url
        response = requests.head(url, timeout=10)
        if 300 <= response.status_code < 400:
            return expand_url(response.headers["Location"])
        else:
            return response.url
    except Exception as e:
        print(e)
        return url


def ommit_long_url(url: str, length=32) -> str:
    """入力したURL文字列のうち先頭29文字と末尾に...をつけた32文字を返す。
    ただし、入力した文字列が32文字以下の場合はそのまま返す
    """
    if len(url) > length:
        return url[:length-3] + "..."
    return url


def get_byte_length(text: str) -> int:
    """入力した文字列のバイト長を返す"""
    return len(text.encode("utf-8"))
