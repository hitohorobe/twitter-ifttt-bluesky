import json
import os
import re
from datetime import datetime
from logging import getLogger
from typing import Optional

import requests
import requests_cache
from pydantic import HttpUrl
from requests import ConnectionError, HTTPError, Timeout

from app.models.bluesky_models import (
    Blob,
    CreateRecordPayload,
    Embed,
    External,
    Facet,
    Feature,
    ImageUploadResponse,
    Index,
    LabelEnum,
    Labels,
    LabelValue,
    LoginResponse,
    Record,
    Ref,
)
from app.models.exception_models import (
    BlueskyDomainError,
    ImageUploadError,
    LoginError,
    PostFailedError,
)
from app.settings.bluesky_settings import (
    BLUESKY_API_DOMAIN,
    DEFAULT_CLIENT_NAME,
    LIMIT_MESSAGE_LENGTH,
    TZ,
)
from app.settings.sensitive_url_list import PORN_URL_LIST
from app.utils.ogp_utils import get_ogp
from app.utils.url_utils import expand_url, extract_url, get_byte_length, ommit_long_url

logger = getLogger(__name__)
requests_cache.install_cache("bluesky_cache", backend="sqlite", expire_after=300)
CLIENT_NAME = os.getenv("CLIENT_NAME", DEFAULT_CLIENT_NAME)


class Bluesky:
    """
    Bluesky の操作クラス
    - login: ログイン
    - sensitive_url_check: センシティブなURLかどうかをチェック
    - upload_image: 画像アップロード
    - make_record: post用のペイロード作成
    - post_record: 新規ポスト
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def login(cls, handle: str, app_password: str) -> Optional[LoginResponse]:
        """ログインしてアクセストークンを取得する"""

        # ハンドルの先頭に@がついていれば削除
        if handle.startswith("@"):
            handle = handle[1:]

        login_endpoint = (
            f"https://{BLUESKY_API_DOMAIN}/xrpc/com.atproto.server.createSession"
        )
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(
            {
                "identifier": handle,
                "password": app_password,
            }
        )

        try:
            response = requests.post(
                login_endpoint, data=payload, headers=headers, timeout=10
            )
            if response.status_code != 200:
                raise LoginError

            response_obj = json.loads(response.text)
            return LoginResponse(
                did=response_obj["did"],
                access_jwt=response_obj["accessJwt"],
            )

        except ConnectionError as e:
            logger.error(e)
            raise BlueskyDomainError

        except Timeout as e:
            logger.error(e)
            raise LoginError

        except HTTPError as e:
            logger.error(e)
            raise LoginError

        except Exception as e:
            logger.error(e)
            raise LoginError

    @classmethod
    def sensitive_url_check(cls, url: str) -> Optional[LabelEnum]:
        """センシティブなURLかどうかをチェックする"""
        for sensitive_url in PORN_URL_LIST:
            if sensitive_url in url:
                return LabelEnum.porn
        return None

    @classmethod
    def upload_image(
        cls, login_response: LoginResponse, image_url: str
    ) -> Optional[ImageUploadResponse]:
        """画像をblob形式でアップロードして参照情報を取得する"""

        image_endpoiiint = (
            f"https://{BLUESKY_API_DOMAIN}/xrpc/com.atproto.repo.uploadBlob"
        )

        # 画像のURLにアクセスしてBLOBとして保存する
        image_response = None

        # ウェブサイト側の設定ミスで指定されているリンクから画像が取得できない場合があるため、
        # その場合は例外で停止させず None を返す
        try:
            image_response = requests.get(image_url, timeout=10)

        except Exception as e:
            logger.error(e)
            return None

        if image_response is None:
            return None

        blobs = image_response.content
        headers = {
            "Authorization": f"Bearer {login_response.access_jwt}",
            "Content-Type": "application/octet-stream",
        }
        try:
            response = requests.post(
                image_endpoiiint, data=blobs, headers=headers, timeout=10
            )

            response_obj = json.loads(response.text)
            return ImageUploadResponse(
                blob=Blob(
                    types="blob",
                    ref=Ref(link=response_obj["blob"]["ref"]["$link"]),
                    mime_type=response_obj["blob"]["mimeType"],
                    size=response_obj["blob"]["size"],
                )
            )

        except ConnectionError as e:
            logger.error(e)
            raise BlueskyDomainError

        except Timeout as e:
            logger.error(e)
            raise ImageUploadError

        except HTTPError as e:
            logger.error(e)
            raise ImageUploadError

        except Exception as e:
            logger.error(e)
            raise ImageUploadError

    @classmethod
    def make_record(
        cls,
        login_response: LoginResponse,
        text: str,
        link_to_tweet: Optional[str] = None,
    ) -> CreateRecordPayload:
        """
        新規ポスト用のペイロードを作成する
        - URLを抽出
        - OGPを取得
        - OGP画像があり、かつセンシティブリストに含まれるURLの場合、センシティブラベルを付与
        - OGP画像をBlueskyにアップロードして参照情報を取得
        - ペイロードを組み立て
        """

        urls = extract_url(text)
        facets: list[Facet] = []
        embed: list[Embed] = []
        labels = None

        # 重複するURLを削除
        urls = list(dict.fromkeys(urls))

        for url in urls:
            # t.co を展開
            expanded_url = expand_url(url)

            # 展開したURLで元のURLを置換し、さらに省略表示にする
            omitted_url = ommit_long_url(url=expanded_url, length=32)
            text = text.replace(url, omitted_url)
            matched_all = re.finditer(re.escape(omitted_url), text)

            for matched in matched_all:
                # リッチテキストでリンクを表現する
                # 終了位置が文字数上限を超えている場合はリッチテキストを作成しない
                if matched.end() > LIMIT_MESSAGE_LENGTH:
                    continue

                else:
                    start_string = matched.start()
                    byte_start = get_byte_length(text[:start_string])
                    byte_end = byte_start + get_byte_length(omitted_url)

                    facet = Facet(
                        index=Index(byte_start=byte_start, byte_end=byte_end),
                        features=[
                            Feature(
                                types="app.bsky.richtext.facet#link",
                                uri=HttpUrl(expanded_url),
                            ),
                        ],
                    )
                    facets.append(facet)

            ogp = get_ogp(expanded_url)
            if ogp is None:
                continue

            image_upload_response = None
            if ogp.image:
                image_upload_response = Bluesky.upload_image(
                    login_response, str(ogp.image)
                )

            embed.append(
                Embed(
                    types="app.bsky.embed.external",
                    external=External(
                        uri=HttpUrl(expanded_url),
                        title=ogp.title if ogp.title else "",
                        description=ogp.description if ogp.description else "",
                        thumb=(
                            image_upload_response.blob
                            if image_upload_response
                            else None
                        ),
                    ),
                )
            )

        # すべてのリンクを省略表示した後、テキストが文字数上限を超えていれば
        # 文字数上限-3文字になるようテキストを切り詰めたのち、参照リンクを付与
        if len(text) > LIMIT_MESSAGE_LENGTH:
            link_text = "...\nExpand"
            text = text[: LIMIT_MESSAGE_LENGTH - len(link_text)]
            byte_start = get_byte_length(text)
            byte_end = byte_start + get_byte_length(link_text)
            text += link_text
            if link_to_tweet:
                facet = Facet(
                    index=Index(byte_start=byte_start, byte_end=byte_end),
                    features=[
                        Feature(
                            types="app.bsky.richtext.facet#link",
                            uri=HttpUrl(link_to_tweet),
                        ),
                    ],
                )
                facets.append(facet)

        # Embed が存在し、かつリストの最後の要素がセンシティブリストに含まれるURLを持っている場合、
        # センシティブラベルを付与
        if embed and embed[-1] is not None and embed[-1].external is not None:
            label_value = Bluesky.sensitive_url_check(str(embed[-1].external.uri))
            if label_value:
                labels = Labels(
                    types="com.atproto.label.defs#selfLabels",
                    values=[LabelValue(val=label_value)],
                )

        record = CreateRecordPayload(
            repo=login_response.did,
            collection="app.bsky.feed.post",
            record=Record(
                text=text,
                created_at=datetime.now(TZ).isoformat(),
                facets=facets,
                embed=embed[-1] if embed else None,
                labels=labels,
                via=CLIENT_NAME,
            ),
        )

        return record

    @classmethod
    def post_record(
        cls, login_response: LoginResponse, record: CreateRecordPayload
    ) -> CreateRecordPayload:
        """新規ポストを投稿する"""

        post_endpoint = (
            f"https://{BLUESKY_API_DOMAIN}/xrpc/com.atproto.repo.createRecord"
        )

        headers = {
            "Authorization": f"Bearer {login_response.access_jwt}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                post_endpoint,
                data=record.model_dump_json(by_alias=True, exclude_none=True),
                headers=headers,
                timeout=10,
            )
            return record

        except ConnectionError as e:
            logger.error(e)
            raise BlueskyDomainError

        except Timeout as e:
            logger.error(e)
            raise PostFailedError

        except HTTPError as e:
            logger.error(e)
            raise PostFailedError

        except Exception as e:
            logger.error(e)
            raise PostFailedError
